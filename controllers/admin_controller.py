from models.admin_model import (
    get_all_users, delete_user_by_id, get_system_stats, 
    verify_admin_credentials, create_admin, get_all_admins, delete_admin
)
from models.transaction_model import get_all_transactions_global, delete_transaction

def authenticate_admin(username, password):
    return verify_admin_credentials(username, password)

def fetch_all_users():
    return get_all_users()

def remove_user(user_id):
    return delete_user_by_id(user_id)

def fetch_stats():
    return get_system_stats()

def fetch_all_admins():
    return get_all_admins()

def add_new_admin(username, password):
    return create_admin(username, password)

def remove_admin(admin_id):
    return delete_admin(admin_id)

def fetch_global_transactions(transaction_type=None):
    return get_all_transactions_global(transaction_type)

def remove_transaction(tx_id):
    return delete_transaction(tx_id)

from models.transaction_model import get_user_transactions_with_counterparty # New import

def fetch_user_transactions_with_counterparty(user_id):
    return get_user_transactions_with_counterparty(user_id)