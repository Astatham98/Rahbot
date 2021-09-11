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
        name = member.name.replace(' ', '_')
        id = str(member.id)

        self.cur.execute(
            'SELECT played FROM leaderboard l WHERE l.id = %s', [id]
        )
        games_played = self.cur.fetchone()
        if games_played:
            new_played = games_played[0] + 1

            self.cur.execute('UPDATE leaderboard SET played = %s WHERE id = %s', (new_played, id))

        else:
            self.cur.execute(
                'INSERT INTO leaderboard (ID,NAME,PLAYED) \
                             VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                (id, name, 0)
            )

        self.conn.commit()
        self.conn.close()
