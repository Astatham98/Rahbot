import sqlite3
import os
from datetime import datetime, timezone


class Database:
    def __init__(self, db_path: str = None):
        """Initialize SQLite database connection.
        
        Args:
            db_path: Path to the SQLite database file. Defaults to 'rahbot.db' in the
                    same directory as this script.
        """
        if db_path is None:
            base_dir = os.path.dirname(os.path.realpath(__file__))
            db_path = os.path.join(base_dir, "rahbot.db")
        self.db_path = db_path
        self.conn = None
        self.cur = None

    def open(self):
        """Open database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.cur = self.conn.cursor()

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()

    def insert_into_leaderboard(self, member):
        """Insert or update a player in the leaderboard.
        
        Args:
            member: Object with 'name' and 'id' attributes
        """
        self.open()
        try:
            name = member.name
            member_id = str(member.id)
            
            # Check if player exists
            self.cur.execute(
                "SELECT played FROM leaderboard WHERE id = ?", (member_id,)
            )
            games_played = self.cur.fetchone()
            
            if games_played:
                new_played = games_played[0] + 1
                self.cur.execute(
                    "UPDATE leaderboard SET played = ? WHERE id = ?",
                    (new_played, member_id)
                )
            else:
                self.cur.execute(
                    "INSERT INTO leaderboard (id, name, played) VALUES (?, ?, ?)",
                    (member_id, name, 1)
                )
            
            self.conn.commit()
        finally:
            self.close()

    def ensure_player_in_leaderboard(self, member_id, member_name):
        """Ensure a player exists in leaderboard with 0 games played.

        Does not overwrite existing rows.
        """
        self.open()
        try:
            self.cur.execute(
                "INSERT OR IGNORE INTO leaderboard (id, name, played) VALUES (?, ?, ?)",
                (str(member_id), member_name, 0),
            )
            self.conn.commit()
        finally:
            self.close()

    def get_players_and_games_played(self):
        """Get all players and their games played, ordered by games descending.
        
        Returns:
            Tuple of (ids, names, played) - three lists
        """
        self.open()
        try:
            self.cur.execute(
                "SELECT id, name, played FROM leaderboard ORDER BY played DESC"
            )
            board = self.cur.fetchall()
            ids, names, played = [], [], []
            for row in board:
                ids.append(row[0])
                names.append(row[1])
                played.append(row[2])
            return ids, names, played
        finally:
            self.close()

    def modify_player(self, member, amount: int, remove: bool = False):
        """Modify a player's games played count.
        
        Args:
            member: Member mention string or ID
            amount: Amount to set or subtract
            remove: If True, subtract from current; otherwise set to amount
        """
        self.open()
        try:
            member_id = self.parse_mention(member)
            
            if not remove:
                self.cur.execute(
                    "UPDATE leaderboard SET played = ? WHERE id = ?",
                    (amount, member_id)
                )
            else:
                self.cur.execute(
                    "UPDATE leaderboard SET played = played - ? WHERE id = ?",
                    (amount, member_id)
                )
            
            self.conn.commit()
        finally:
            self.close()

    def immune(self, member_id):
        """Check if a member has immunity.
        
        Args:
            member_id: The member's ID
            
        Returns:
            Immunity status or None
        """
        self.open()
        try:
            self.cur.execute(
                "SELECT immunity FROM games WHERE id = ?", (member_id,)
            )
            immunity = self.cur.fetchone()
            return immunity[0] if immunity else None
        finally:
            self.close()

    def set_immune(self, member_id):
        """Set a member as immune.
        
        Args:
            member_id: The member's ID
        """
        self.open()
        try:
            self.cur.execute(
                "UPDATE games SET immunity = 1 WHERE id = ?", (member_id,)
            )
            self.conn.commit()
        finally:
            self.close()

    def reset_immunity(self):
        """Reset all immunity flags to False."""
        self.open()
        try:
            self.cur.execute("UPDATE games SET immunity = 0 WHERE immunity = 1")
            self.conn.commit()
        finally:
            self.close()

    def find_teammates(self, member_id):
        """Find teammates from the same game who don't have immunity.
        
        Args:
            member_id: The member's ID
            
        Returns:
            List of tuples containing (id, team)
        """
        self.open()
        try:
            self.cur.execute(
                "SELECT game_id, team FROM games WHERE id = ?", (member_id,)
            )
            output = self.cur.fetchone()
            if not output:
                return []
            gameid, team = output[0], output[1]
            
            self.cur.execute(
                "SELECT id FROM games WHERE game_id = ? AND immunity = 0 AND team = ?",
                (gameid, team)
            )
            return self.cur.fetchall()
        finally:
            self.close()

    def games(self, member_id, game_id, team):
        """Record a player's game participation.
        
        Args:
            member_id: The member's ID
            game_id: The game ID
            team: The team name ('red' or 'blue')
        """
        self.open()
        try:
            # Check if member has immunity
            self.cur.execute(
                "SELECT immunity FROM games WHERE id = ?", (member_id,)
            )
            immunity = self.cur.fetchone()
            
            if immunity is not None:
                self.cur.execute(
                    "UPDATE games SET game_id = ?, team = ? WHERE id = ?",
                    (game_id, team, member_id)
                )
            else:
                self.cur.execute(
                    "INSERT INTO games (id, game_id, team, immunity) VALUES (?, ?, ?, 0)",
                    (member_id, game_id, team)
                )
            
            self.conn.commit()
        finally:
            self.close()

    def insert_into_users(self, member_id, linked_profile, steam_profile, verified):
        """Insert or update a user's profile.
        
        Args:
            member_id: The member's ID
            linked_profile: Link to their profile (e.g., ETF2L)
            steam_profile: Steam profile link
            verified: Boolean indicating if verified
        """
        self.open()
        try:
            dt = datetime.now(timezone.utc).isoformat()
            self.cur.execute(
                "INSERT OR REPLACE INTO users (id, linkedProfile, steam, dateRegistered, verified) VALUES (?, ?, ?, ?, ?)",
                (member_id, linked_profile, steam_profile, dt, verified)
            )
            self.conn.commit()
        finally:
            self.close()

    def get_user_accounts(self, account_type, account_link):
        """Get user account details by account type.
        
        Args:
            account_type: Column name to search ('id', 'linkedProfile', 'steam')
            account_link: The value to search for
            
        Returns:
            Tuple of user data or None
        """
        self.open()
        try:
            # Validate column name to prevent SQL injection
            valid_columns = {'id', 'linkedProfile', 'steam'}
            if account_type not in valid_columns:
                return None
                
            self.cur.execute(
                f"SELECT * FROM users WHERE {account_type} = ?", (account_link,)
            )
            return self.cur.fetchone()
        finally:
            self.close()

    def check_user_exists(self, member_id, link):
        """Check if a user exists and if link is already associated.
        
        Args:
            member_id: The member's ID
            link: Profile link to check
            
        Returns:
            Tuple of (exist_and_same, no_user_with_linked_profile)
        """
        self.open()
        try:
            # Check if link is already used
            self.cur.execute(
                "SELECT id FROM users WHERE linkedProfile = ?", (link,)
            )
            used_id = self.cur.fetchone()
            
            no_user_with_linked_profile = used_id is None
            if not no_user_with_linked_profile:
                used_id = used_id[0]
                
            exist_and_same = used_id == member_id
            no_user_with_linked_profile = used_id is None
            
            # Check if member_id exists in DB
            self.cur.execute(
                "SELECT id FROM users WHERE id = ?", (member_id,)
            )
            in_db = self.cur.fetchone()
            if in_db is not None:
                in_db = in_db[0]
                
            if not exist_and_same and in_db is not None:
                no_user_with_linked_profile = False
            
            return exist_and_same, no_user_with_linked_profile
        finally:
            self.close()

    def get_warned_player(self, member_id):
        """Get all warnings for a player.
        
        Args:
            member_id: The member's ID
            
        Returns:
            List of warning tuples
        """
        self.open()
        try:
            self.cur.execute(
                "SELECT * FROM warnings WHERE id = ?", (member_id,)
            )
            return self.cur.fetchall()
        finally:
            self.close()

    def warn_player(self, member_id, duration, reason=""):
        """Add a warning for a player.
        
        Args:
            member_id: The member's ID
            duration: Warning duration in minutes
            reason: Reason for the warning
        """
        self.open()
        try:
            self.cur.execute(
                "INSERT INTO warnings (id, banTime, reason) VALUES (?, ?, ?)",
                (member_id, duration, reason)
            )
            self.conn.commit()
        finally:
            self.close()

    def create_leaderboard_table(self):
        """Create the leaderboard table if it doesn't exist."""
        self.open()
        try:
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS leaderboard("
                "id TEXT PRIMARY KEY, "
                "name TEXT, "
                "played INTEGER DEFAULT 0)"
            )
            self.conn.commit()
        finally:
            self.close()

    def create_games_table(self):
        """Create the games table if it doesn't exist."""
        self.open()
        try:
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS games("
                "id TEXT PRIMARY KEY, "
                "game_id TEXT, "
                "team TEXT, "
                "immunity INTEGER DEFAULT 0)"
            )
            self.conn.commit()
        finally:
            self.close()

    def create_users_table(self):
        """Create the users table if it doesn't exist."""
        self.open()
        try:
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS users("
                "id TEXT PRIMARY KEY, "
                "linkedProfile TEXT, "
                "steam TEXT, "
                "dateRegistered TEXT, "
                "verified INTEGER)"
            )
            self.conn.commit()
        finally:
            self.close()

    def create_warnings_table(self):
        """Create the warnings table if it doesn't exist."""
        self.open()
        try:
            self.cur.execute(
                "CREATE TABLE IF NOT EXISTS warnings("
                "id TEXT, "
                "banTime INTEGER, "
                "reason TEXT)"
            )
            self.conn.commit()
        finally:
            self.close()

    def parse_mention(self, mention: str):
        """Parse a Discord mention string to extract the ID.
        
        Args:
            mention: Discord mention string (e.g., '<@!123456789>' or '<@123456789>')
            
        Returns:
            The extracted ID string
        """
        id_str = mention.replace(">", "")
        id_str = id_str.replace("<@", "")
        # Handle nickname mentions
        if "!" in id_str:
            id_str = id_str.split("!")[-1]
        return id_str
