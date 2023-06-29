import sqlite3

class DbFunctions:
    
    @staticmethod
    def connect_to_database(database_name):
        connection = sqlite3.connect(database_name)
        return connection

    #save message to db
    @staticmethod
    def save_message(config_values, message_text, user_id, message_id, chat_id):
        table_prefix_msg = config_values['table_prefix_msg']
        connection = config_values['connection']

        query = f'CREATE TABLE IF NOT EXISTS "{table_prefix_msg}{chat_id}" \
                (message_id INTEGER PRIMARY KEY, user_id INTEGER, message_text TEXT, deleted INTEGER)'
        connection.execute(query)
        connection.commit()
        
        #we don't save message text
        data = (message_id, user_id, "", 0)
        query = f'REPLACE INTO "{table_prefix_msg}{chat_id}" (message_id, user_id, message_text, deleted) VALUES (?, ?, ?, ?)'
        connection.execute(query, data)
        connection.commit()

        return True

    #work with user
    @staticmethod
    def save_user(config_values, message_text, user_id, message_id, chat_id):
        table_prefix_user = config_values['table_prefix_user']
        connection = config_values['connection']

        query = f'CREATE TABLE IF NOT EXISTS "{table_prefix_user}{chat_id}" \
                (user_id INTEGER PRIMARY KEY, message_hash TEXT, human INTEGER, messages_count INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
        connection.execute(query)
        connection.commit()
        
        #messages count = 0, human = 0. TODO: fix it
        data = (user_id, hash(message_text[:1000]), 0,0,)
        query = f'REPLACE INTO "{table_prefix_user}{chat_id}" (user_id, message_hash, human, messages_count) VALUES (?, ?, ?, ?)'
        connection.execute(query, data)
        connection.commit()

        return True
