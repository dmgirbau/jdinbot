import sqlite3, aiosqlite



class DataBase:


    def __init__(self):
        conn = sqlite3.connect('jdin_bot.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                jdin_balance REAL DEFAULT 0.0,
                pedjbono_id INTEGER,
                unique_code TEXT UNIQUE,
                solana_account TEXT,
                pending_request INTEGER DEFAULT 0
            )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                tx_id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_user_id INTEGER,
                to_user_id INTEGER,
                amount REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (from_user_id) REFERENCES users(user_id),
                FOREIGN KEY (to_user_id) REFERENCES users(user_id)
            )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lojdin_statistics (
                lojdin_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                bet_amount REAL,
                outcome REAL,
                rolls INTEGER,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS solana_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                solana_address TEXT,
                type TEXT CHECK(type IN ('existing', 'new')),
                status TEXT DEFAULT 'pending',
                fee REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_at TIMESTAMP)
            ''')
            
        cursor.execute('''CREATE TABLE IF NOT EXISTS solana_accounts (
                user_id INTEGER PRIMARY KEY,
                solana_address TEXT UNIQUE,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
        conn.commit()
        conn.close()


# Database connection management
_connection = None

async def get_db_connection():
    """
    Get a shared database connection. This function implements a connection pool pattern
    where we maintain a single connection to the database that is reused across requests.
    
    Returns:
        aiosqlite.Connection: An async SQLite connection object
    """
    global _connection
    if _connection is None:
        _connection = await aiosqlite.connect("jdin_bot.db", check_same_thread=False)
    return _connection


class ConnectionManager:
    """
    A proper async context manager for database connections.
    
    This class implements the asynchronous context manager protocol to safely manage
    database connections using the 'async with' syntax. It reuses a single connection
    from the connection pool to avoid the 'threads can only be started once' error.
    
    Example:
        async with connection() as conn:
            cursor = await conn.execute("SELECT * FROM users")
            result = await cursor.fetchone()
    """
    
    def __init__(self):
        self.conn = None
        
    async def __aenter__(self):
        """
        Enter the async context and return the database connection.
        
        Returns:
            aiosqlite.Connection: A database connection from the pool
        """
        self.conn = await get_db_connection()
        return self.conn
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the async context. We don't close the connection as it's shared in the pool.
        
        Args:
            exc_type: Exception type if an exception was raised
            exc_val: Exception value if an exception was raised
            exc_tb: Exception traceback if an exception was raised
        """
        # We don't close the connection as it's shared
        pass


def connection():
    """
    Return a connection context manager that can be used with 'async with'.
    This is a factory function that creates a new ConnectionManager instance.
    
    Returns:
        ConnectionManager: A connection manager that implements the async context manager protocol
    """
    return ConnectionManager()