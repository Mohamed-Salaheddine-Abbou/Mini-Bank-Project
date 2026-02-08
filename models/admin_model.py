from config.db import get_connection
from utils.security import hash_password, verify_password

def _init_admins_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL
        )
    """)
    
    # Check for default admin
    cursor.execute("SELECT id FROM admins WHERE username = 'admin'")
    if not cursor.fetchone():
        pw_hash = hash_password("admin123")
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (%s, %s)", ("admin", pw_hash))
        
    conn.commit()
    cursor.close()
    conn.close()

try:
    _init_admins_table()
except Exception:
    pass

def verify_admin_credentials(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admins WHERE username = %s", (username,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if row:
        return verify_password(password, row[0])
    return False

def create_admin(username, password):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        pw_hash = hash_password(password)
        cursor.execute("INSERT INTO admins (username, password_hash) VALUES (%s, %s)", (username, pw_hash))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_admins():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM admins")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def delete_admin(admin_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM admins WHERE id = %s", (admin_id,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, phone, account_number, balance FROM users")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def delete_user_by_id(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Delete dependencies first (Foreign Keys)
        cursor.execute("DELETE FROM notifications WHERE user_id = %s", (user_id,))
        cursor.execute("DELETE FROM transactions WHERE user_id = %s", (user_id,))
        
        # Delete the user
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        
        conn.commit()
        return True
    except Exception as e:
        print(f"Delete Error: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()

def get_system_stats():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(balance) FROM users")
    total_balance = cursor.fetchone()[0] or 0.0
    
    cursor.close()
    conn.close()
    return user_count, total_balance