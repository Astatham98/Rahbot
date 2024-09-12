import os
import configparser
import psycopg2
from datetime import datetime, timezone
from functools import wraps


def pre_post_call(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._pre_call()
        try:
            result = method(self, *args, **kwargs)
            return result
        finally:
            self._post_call()

    return wrapper


class Database:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read("config.ini")
        self.DATABASE_HOST = (
            os.environ.get("DATABASE_HOST")
            if os.environ.get("DATABASE_HOST") is not None
            else config.get("DATABASE", "DATABASE_HOST")
        )
        self.DATABASE_USER = (
            os.environ.get("DATABASE_USER")
            if os.environ.get("DATABASE_USER") is not None
            else config.get("DATABASE", "DATABASE_USER")
        )
        self.DATABASE_PASSWORD = (
            os.environ.get("DATABASE_PASSWORD")
            if os.environ.get("DATABASE_PASSWORD") is not None
            else config.get("DATABASE", "DATABASE_PASSWORD")
        )
        self.DATABASE_NAME = (
            os.environ.get("DATABASE_NAME")
            if os.environ.get("DATABASE_NAME") is not None
            else config.get("DATABASE", "DATABASE_NAME")
        )
        self.cur = None

    def _pre_call(self):
        self.open()

    def _post_call(self):
        self.close()

    def close(self):
        self.conn.close()

    def open(self):
        self.conn = psycopg2.connect(
            dbname=self.DATABASE_NAME,
            user=self.DATABASE_USER,
            password=self.DATABASE_PASSWORD,
            host=self.DATABASE_HOST,
        )
        self.cur = self.conn.cursor()

    @pre_post_call
    def insert_into_leaderboard(self, member):
        name = member.name
        id = str(member.id)
        print(id)

        self.cur.execute("SELECT played FROM leaderboard l WHERE l.id = %s", [id])
        games_played = self.cur.fetchone()
        if games_played:
            new_played = games_played[0] + 1

            self.cur.execute(
                "UPDATE leaderboard SET played = %s WHERE id = %s", (new_played, id)
            )

        else:
            self.cur.execute(
                "INSERT INTO leaderboard (ID,NAME,PLAYED) \
                             VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
                (id, name, 1),
            )

        self.conn.commit()

    @pre_post_call
    def get_players_and_games_played(self):
        self.cur.execute("SELECT * FROM leaderboard ORDER BY leaderboard.played DESC")
        board = self.cur.fetchall()
        name, played, id = [], [], []
        for row in board:
            id.append(row[0])
            name.append(row[1])
            played.append(row[2])
        return id, name, played

    @pre_post_call
    def modify_player(self, member, amount: int, remove=False):
        id = self.parse_mention(member)

        if not remove:
            self.cur.execute(
                "UPDATE leaderboard SET played = %s WHERE id = %s", (amount, id)
            )
        else:
            self.cur.execute(
                "UPDATE leaderboard SET played = played - %s WHERE id = %s",
                (amount, id),
            )

        self.conn.commit()

    @pre_post_call
    def immune(self, member_id):
        self.cur.execute(
            "SELECT immunity FROM leaderboard l WHERE l.id = %s", [member_id]
        )
        immunity = self.cur.fetchone()
        if immunity is not None:
            return immunity[0]
        return None

    @pre_post_call
    def set_immune(self, member_id):
        self.cur.execute("UPDATE games SET immunity = true WHERE id = %s", [member_id])
        self.conn.commit()

    @pre_post_call
    def reset_immunity(self):
        self.cur.execute("UPDATE games SET immunity = False WHERE immunity = True")
        self.conn.commit()

    @pre_post_call
    def find_teammates(self, id):
        self.cur.execute("SELECT gameID, team from games WHERE id = %s", [id])
        output = self.cur.fetchone()
        gameid, team = output[0], output[1]

        self.cur.execute(
            "SELECT id FROM games g WHERE g.gameID = %s and g.immunity = %s and team = %s",
            (gameid, False, team),
        )
        return self.cur.fetchall()

    @pre_post_call
    def games(self, member_id, game_id, team):
        self.cur.execute("SELECT immunity FROM games g WHERE g.id = %s", [member_id])
        immunity = self.cur.fetchone()

        if immunity is not None:
            self.cur.execute(
                "UPDATE games SET gameID = %s, team = %s WHERE id = %s",
                (game_id, team, member_id),
            )

        else:
            self.cur.execute(
                "INSERT INTO games (id,gameID,team,immunity) \
                             VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
                (member_id, game_id, team, False),
            )

        self.conn.commit()

    @pre_post_call
    def insert_into_users(self, member_id, linkedProfile, steamProfile, verified):
        dt = datetime.now(timezone.utc)
        self.cur.execute(
            "INSERT INTO users (id,linkedProfile,steam,dateRegistered,verified) VALUES (%s, %s, %s, %s, %s)",
            (member_id, linkedProfile, steamProfile, dt, verified),
        )
        self.conn.commit()
        
    @pre_post_call
    def get_user_accounts(self, account_type, account_link):
        self.cur.execute(
            f"SELECT * from users WHERE users.{account_type} = %s", [account_link]
        )
        #[id, etf2l, steam, registered, verified]
        return self.cur.fetchone()

    @pre_post_call
    def check_user_exists(self, member_id, link):
        # check if the user link exists in the db
        try:
            self.cur.execute(
                "SELECT id FROM users WHERE users.linkedProfile = %s", [link]
            )
        except Exception as e:
            print(f"Error {e}")
            self.conn.rollback()
        used_id = self.cur.fetchone()
        no_user_with_linkedProfile = used_id == None
        if not no_user_with_linkedProfile:
            used_id = used_id[0]
        exist_and_same = used_id == member_id
        no_user_with_linkedProfile = used_id == None
        # if users id exists in db but trying to link with another account
        self.cur.execute("SELECT id FROM users WHERE users.id = %s", [member_id])
        in_db = self.cur.fetchone()
        if in_db is not None:
            in_db = in_db[0]
        if not exist_and_same and in_db is not None:
            no_user_with_linkedProfile = False

        return exist_and_same, no_user_with_linkedProfile

    @pre_post_call
    def get_warned_player(self, id):
        self.cur.execute("SELECT * from warnings where warnings.id = %s", [id])
        return self.cur.fetchall()

    @pre_post_call
    def warn_player(self, id, duration, reason=""):
        self.cur.execute(
            "INSERT INTO WARNINGS (id, banTime, reason) VALUES (%s, %s, %s)",
            (id, duration, reason),
        )
        self.conn.commit()

    @pre_post_call
    def create_leaderboard_table(self):
        # id name played
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS leaderboard(id VARCHAR(255) PRIMARY KEY,name VARCHAR(255), played INTEGER)"
        )
        self.conn.commit()

    @pre_post_call
    def create_games_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS games(id VARCHAR(255) PRIMARY KEY, game_id VARCHAR(255), team VARCHAR(4), immunity BOOLEAN)"
        )
        self.conn.commit()

    @pre_post_call
    def create_users_table(self):
        # id linkedProfile steamProfile dateRegistered Verified
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS users(id VARCHAR(255) PRIMARY KEY, linkedProfile VARCHAR(255), steam VARCHAR(255), dateRegistered TIMESTAMP, verified BOOLEAN)"
        )
        self.conn.commit()

    @pre_post_call
    def create_warnings_table(self):
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS warnings(id VARCHAR(255), banTime INTEGER, reason VARCHAR(255))"
        )
        self.conn.commit()

    def parse_mention(self, mention: str):
        """turns a mention into an id string"""
        id = mention.replace(">", "")
        id = id.replace("<@", "")
        return id.split("!")[-1]
