import re
import sqlite3
from db_functions_class import DbFunctions
from rules_class import Rules

class Training:
    
    @staticmethod
    def train_good(config_values):
        connection = config_values['connection']
        query = f'SELECT user_id,text FROM "good_messages"'
        result = connection.execute(query)

        row = result.fetchone()
        while row is not None:
            user_id = row[0]
            message_text = row[1]
            Rules.message_check(config_values, message_text, user_id, 0, 0)
            row = result.fetchone()

        result.close()

    def train_bad(config_values):
        connection = config_values['connection']
        query = f'SELECT user_id,text FROM "bad_messages"'
        result = connection.execute(query)

        row = result.fetchone()
        while row is not None:
            user_id = row[0]
            message_text = row[1]
            Rules.message_check(config_values, message_text, user_id, 0, 0)
            row = result.fetchone()

        result.close()
