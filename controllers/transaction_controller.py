from config.db import get_connection
from models.user_model import get_user_by_account_number, get_user_by_id
from models.transaction_model import (
    get_balance,
    update_balance,
    insert_transaction,
    get_transactions,
    get_daily_transfer_count,
    transfer_funds
)


def deposit(user_id, amount):
    if amount <= 0:
        return False, "Invalid deposit amount"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        update_balance(cursor, user_id, amount)
        insert_transaction(cursor, user_id, "DEPOSIT", amount)

        conn.commit()
        return True, "Deposit successful"

    except Exception as e:
        conn.rollback()
        return False, "Deposit failed"

    finally:
        cursor.close()
        conn.close()


def withdraw(user_id, amount):
    if amount <= 0:
        return False, "Invalid withdrawal amount"

    current_balance = get_balance(user_id)

    if current_balance is None:
        return False, "User not found"

    if amount > current_balance:
        return False, "Insufficient balance"

    conn = get_connection()
    cursor = conn.cursor()

    try:
        update_balance(cursor, user_id, -amount)
        insert_transaction(cursor, user_id, "WITHDRAW", amount)

        conn.commit()
        return True, "Withdrawal successful"

    except Exception:
        conn.rollback()
        return False, "Withdrawal failed"

    finally:
        cursor.close()
        conn.close()


def get_account_history(user_id):
    return get_transactions(user_id)

def send_money(sender_id, receiver_account, amount):
    if amount <= 0:
        return False, "Invalid amount"

    # 1. Check Daily Limit (Max 3)
    count = get_daily_transfer_count(sender_id)
    if count >= 3:
        return False, "Daily transfer limit (3) reached."

    # 2. Validate Receiver
    receiver_data = get_user_by_account_number(receiver_account)
    if not receiver_data:
        return False, "Receiver account not found."
    
    receiver_id = receiver_data[0]
    if receiver_id == sender_id:
        return False, "Cannot send money to yourself."

    # 3. Check Balance
    current_balance = get_balance(sender_id)
    if current_balance is None or current_balance < amount:
        return False, "Insufficient balance."

    # 4. Get Sender Name for notification
    sender_data = get_user_by_id(sender_id)
    sender_name = sender_data[1] if sender_data else "Unknown"

    # 5. Perform Transfer
    return transfer_funds(sender_id, receiver_id, amount, sender_name)
