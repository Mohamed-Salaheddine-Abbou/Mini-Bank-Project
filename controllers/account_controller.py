from models.user_model import create_user
from utils.validators import is_valid_algerian_phone
from utils.security import (
    generate_account_number,
    generate_password,
    hash_password
)


def open_account(full_name, phone):

    if not full_name or not phone:
        return None, "Full name and phone number are required"

    if not is_valid_algerian_phone(phone):
        return None, "Invalid Algerian phone number"

    account_number = generate_account_number()
    password = generate_password()
    password_hash = hash_password(password)

    try:
        create_user(
            full_name=full_name,
            phone=phone,
            account_number=account_number,
            password_hash=password_hash
        )
    except Exception as e:
        print(f"DEBUG ERROR: {e}")
        if "Duplicate entry" in str(e):
            return None, "Phone number already exists"
        else:
            return None, f"Database Error: {str(e)}"

    return {
        "account_number": account_number,
        "password": password
    }, None
