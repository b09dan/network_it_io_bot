#class to store user data
class User:
    def __init__(self, username = None, last_message_hash = None, message_count = 0, last_message_timestamp = None):
        self.username = username
        self.message_count = message_count
        self.last_message_timestamp = last_message_timestamp
        self.last_message_hash = last_message_hash
