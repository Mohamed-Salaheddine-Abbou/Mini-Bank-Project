from models.notification_model import get_unread_notifications, mark_all_read

def get_my_notifications(user_id):
    return get_unread_notifications(user_id)

def read_notifications(user_id):
    mark_all_read(user_id)