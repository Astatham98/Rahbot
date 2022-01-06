import os
import psycopg2
import configparser


class Database:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        DATABASE_URL = os.environ.get('DATABASE_URL') if os.environ.get('DATABASE_URL') is not None else config.get(
            'KEYS', 'DATABASE')
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cur = self.conn.cursor()

    def insert_into_leaderboard(self, member):
        name = member.name
        id = str(member.id)

        self.cur.execute(
            'SELECT played FROM leaderboard l WHERE l.id = %s', [id]
        )
        games_played = self.cur.fetchone()
        print(games_played, name)
        if games_played:
            new_played = games_played[0] + 1

            self.cur.execute('UPDATE leaderboard SET played = %s WHERE id = %s', (new_played, id))

        else:
            self.cur.execute(
                'INSERT INTO leaderboard (ID,NAME,PLAYED) \
                             VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                (id, name, 1)
            )

        self.conn.commit()

    def get_players_and_games_played(self):
        self.cur.execute('SELECT * FROM leaderboard ORDER BY leaderboard.played DESC')
        board = self.cur.fetchall()
        name, played, id = [], [], []
        for row in board:
            id.append(row[0])
            name.append(row[1])
            played.append(row[2])
        return id, name, played

    def modify_player(self, member, amount: int, remove=False):
        id = self.parse_mention(member)

        if not remove:
            self.cur.execute('UPDATE leaderboard SET played = %s WHERE id = %s', (amount, id))
        else:
            self.cur.execute('UPDATE leaderboard SET played = played - %s WHERE id = %s', (amount, id))

        self.conn.commit()
    
    def immune(self, member_id):
        self.cur.execute('SELECT immunity FROM leaderboard l WHERE l.id = %s', [member_id])
        immunity = self.cur.fetchone()
        if immunity is not None:
            return immunity[0]
        return None
    
    def set_immune(self, member_id):
        self.cur.execute('UPDATE leaderboard SET immunity = true WHERE id = %s', [member_id])
        self.conn.commit()

    def reset_immunity(self):
        self.cur.execute('UPDATE leaderboard SET immunity = false WHERE immunity = true')
        self.conn.commit()

    def parse_mention(self, mention: str):
        """turns a mention into an id string"""
        id = mention.replace('>', '')
        return id.split('!')[-1]
        