import re
from config.settings import ALGERIAN_PHONE_REGEX

def is_valid_algerian_phone(phone):
    return re.match(ALGERIAN_PHONE_REGEX, phone) is not None
