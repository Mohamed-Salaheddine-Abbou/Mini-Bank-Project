from config.db import get_connection

def _init_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) UNIQUE NOT NULL,
            account_number VARCHAR(20) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            balance DECIMAL(10, 2) DEFAULT 0.00
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

try:
    _init_users_table()
except Exception:
    pass

def create_user(full_name, phone, account_number, password_hash):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO users (full_name, phone, account_number, password_hash, balance)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (full_name, phone, account_number, password_hash, 0.00))
    
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_account_number(account_number):
    conn = get_connection()
    cursor = conn.cursor()

    sql = "SELECT id, password_hash, full_name FROM users WHERE account_number = %s"
    cursor.execute(sql, (account_number,))
    row = cursor.fetchone()

    cursor.close()
    conn.close()
    return row

def get_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "SELECT id, full_name, account_number FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row
