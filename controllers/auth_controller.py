from models.user_model import get_user_by_account_number
from utils.security import verify_password

def login(account_number, password):
    if not account_number or not password:
        return None, "Please fill all fields"

    user_data = get_user_by_account_number(account_number)

    if not user_data:
        return None, "Invalid account number or password"

    user_id, stored_hash, full_name = user_data

    if verify_password(password, stored_hash):
        return {"id": user_id, "name": full_name}, None
    else:
        return None, "Invalid account number or password"