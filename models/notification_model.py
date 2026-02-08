from config.db import get_connection

def _init_notifications_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            message VARCHAR(255) NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Initialize table on module import
try:
    _init_notifications_table()
except Exception:
    pass

def get_unread_notifications(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = "SELECT message, created_at FROM notifications WHERE user_id = %s AND is_read = FALSE ORDER BY created_at DESC"
    cursor.execute(sql, (user_id,))
    rows = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return rows

def mark_all_read(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = "UPDATE notifications SET is_read = TRUE WHERE user_id = %s AND is_read = FALSE"
    cursor.execute(sql, (user_id,))
    
    conn.commit()
    cursor.close()
    conn.close()