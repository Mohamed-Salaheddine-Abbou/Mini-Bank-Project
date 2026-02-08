from config.db import get_connection

def _init_transactions_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            type VARCHAR(50) NOT NULL,
            amount DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def _fix_transaction_type_length():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE transactions MODIFY COLUMN type VARCHAR(50)")
        conn.commit()
    except Exception:
        pass
    finally:
        cursor.close()
        conn.close()

try:
    _init_transactions_table()
    _fix_transaction_type_length()
except Exception:
    pass

def get_balance(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM users WHERE id = %s",
        (user_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return row[0] if row else None


def get_transactions(user_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT type, amount, created_at
        FROM transactions
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows


def update_balance(cursor, user_id, amount):
   
    sql = """
    UPDATE users
    SET balance = balance + %s
    WHERE id = %s
    """
    cursor.execute(sql, (amount, user_id))


def insert_transaction(cursor, user_id, tx_type, amount):
   
    sql = """
    INSERT INTO transactions (user_id, type, amount)
    VALUES (%s, %s, %s)
    """
    cursor.execute(sql, (user_id, tx_type, amount))

def get_daily_transfer_count(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    sql = """
        SELECT COUNT(*) FROM transactions 
        WHERE user_id = %s AND type = 'TRANSFER_SENT' 
        AND DATE(created_at) = CURDATE()
    """
    cursor.execute(sql, (user_id,))
    count = cursor.fetchone()[0]
    
    cursor.close()
    conn.close()
    return count

def transfer_funds(sender_id, receiver_id, amount, sender_name):
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        update_balance(cursor, sender_id, -amount)
        insert_transaction(cursor, sender_id, "TRANSFER_SENT", amount)
        
        update_balance(cursor, receiver_id, amount)
        insert_transaction(cursor, receiver_id, "TRANSFER_RECEIVED", amount)
        
        sql_notif = "INSERT INTO notifications (user_id, message) VALUES (%s, %s)"
        msg = f"You received {amount:.2f} DA from {sender_name}"
        cursor.execute(sql_notif, (receiver_id, msg))
        
        conn.commit()
        return True, "Transfer successful"
    except Exception as e:
        conn.rollback()
        return False, f"Transfer failed: {str(e)}"
    finally:
        cursor.close()
        conn.close()

def get_all_transactions_global(transaction_type=None):
    conn = get_connection()
    cursor = conn.cursor()
  
    sql = """
        SELECT t.id, u.full_name, t.type, t.amount, t.created_at 
        FROM transactions t
        JOIN users u ON t.user_id = u.id
    """
    params = []
    if transaction_type and transaction_type != "All":
        sql += " WHERE t.type = %s"
        params.append(transaction_type.upper()) # Assuming types are stored in uppercase

    sql += " ORDER BY t.created_at DESC"
    cursor.execute(sql, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

def get_user_transactions_with_counterparty(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    transactions_with_counterparty = []

    # Get all transactions for the user
    cursor.execute("""
        SELECT id, type, amount, created_at
        FROM transactions
        WHERE user_id = %s
        ORDER BY created_at DESC
    """, (user_id,))
    user_transactions = cursor.fetchall()

    for tx_id, tx_type, tx_amount, tx_created_at in user_transactions:
        counterparty_name = "N/A"
        counterparty_account_number = "N/A"

        if tx_type == "TRANSFER_SENT":
            cursor.execute("""
                SELECT u.full_name, u.account_number
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                WHERE t.type = 'TRANSFER_RECEIVED'
                  AND t.amount = %s
                  AND ABS(UNIX_TIMESTAMP(t.created_at) - UNIX_TIMESTAMP(%s)) < 5 -- within 5 seconds
                  AND t.user_id != %s
                LIMIT 1
            """, (tx_amount, tx_created_at, user_id))
            counterparty_info = cursor.fetchone()
            if counterparty_info:
                counterparty_name = counterparty_info[0]
                counterparty_account_number = counterparty_info[1]
        elif tx_type == "TRANSFER_RECEIVED":
            # Find the corresponding TRANSFER_SENT transaction
            cursor.execute("""
                SELECT u.full_name, u.account_number
                FROM transactions t
                JOIN users u ON t.user_id = u.id
                WHERE t.type = 'TRANSFER_SENT'
                  AND t.amount = %s
                  AND ABS(UNIX_TIMESTAMP(t.created_at) - UNIX_TIMESTAMP(%s)) < 5 -- within 5 seconds
                  AND t.user_id != %s
                LIMIT 1
            """, (tx_amount, tx_created_at, user_id))
            counterparty_info = cursor.fetchone()
            if counterparty_info:
                counterparty_name = counterparty_info[0]
                counterparty_account_number = counterparty_info[1]
        
        transactions_with_counterparty.append((tx_id, tx_type, tx_amount, tx_created_at, counterparty_name, counterparty_account_number))

    cursor.close()
    conn.close()
    return transactions_with_counterparty

def delete_transaction(tx_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM transactions WHERE id = %s", (tx_id,))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        cursor.close()
        conn.close()
