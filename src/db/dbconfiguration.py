import sqlite3
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
                approved_at TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS solana_accounts (
                user_id INTEGER PRIMARY KEY,
                solana_address TEXT UNIQUE,
                approved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );''')
        conn.commit()
        conn.close()
def connection():
    return sqlite3.connect("jdin_bot.db", check_same_thread=False).cursor()