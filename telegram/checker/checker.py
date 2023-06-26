import requests
import json
import sqlite3
from rules_class import Rules

#load key-value config, skip # as comments
def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  
                key, value = line.split('=')
                config[key.strip()] = value.strip()
    return config


def user_whitelist_check():
#do check against whitelist and active list
    return True

#work with message: make spam decision
def message_check():
#check message against rules
    return False

#save message to db
def save_message(config_values, message_text, user_id, message_id, chat_id):
    table_prefix_msg = config_values['table_prefix_msg']
    connection = config_values['connection']

    query = f"CREATE TABLE IF NOT EXISTS {table_prefix_msg}{chat_id} (message_id INTEGER PRIMARY KEY, user_id INTEGER, message_text TEXT, deleted INTEGER)"
    connection.execute(query)
    connection.commit()

    data = (message_id, user_id, message_text[:1000], 0)
    query = f"REPLACE INTO {table_prefix_msg}{chat_id} (message_id, user_id, message_text, deleted) VALUES (?, ?, ?, ?)"
    connection.execute(query, data)
    connection.commit()

    return True

#work with user
def save_user(config_values, message_text, user_id, message_id, chat_id):
    table_prefix_user = config_values['table_prefix_user']
    connection = config_values['connection']

    query = f"CREATE TABLE IF NOT EXISTS {table_prefix_user}{chat_id} (user_id INTEGER PRIMARY KEY, message_hash TEXT, human INTEGER, messages_count INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    connection.execute(query)
    connection.commit()
    
    #messages count = 0, human = 0. TODO: fix it
    data = (user_id, hash(message_text[:1000]), 0,0,)
    query = f"REPLACE INTO {table_prefix_user}{chat_id} (user_id, message_hash, human) VALUES (?, ?, ?)"
    connection.execute(query, data)
    connection.commit()

    return True

#work with update
def send_message(config_values, chat_id, text, reply_to_message_id=None):
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    url = f'{api_url}/sendMessage'
    params = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': reply_to_message_id}
    response = requests.post(url, params)
    return response.json()

def process_update(config_values, update):
    print(update)
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'

    if 'message' in update and 'chat' in update['message'] and 'id' in update['message']['chat']:
        chat_id = update['message']['chat']['id']
        if 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            user_id = update['message']['from']['id']

           #### change here user_add(config_values, userid, hash(message_text))
            save_message(config_values, message_text, user_id, message_id, chat_id)
            save_user(config_values, message_text, user_id, message_id, chat_id)
            send_message(config_values, chat_id, f'You said: {message_text}\nYour userid: {user_id}', reply_to_message_id=message_id)

def get_updates(config_values, offset=None):

    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    url = f'{api_url}/getUpdates'

    params = {'offset': offset}
    response = requests.get(url, params)
    return response.json()

def connect_to_database(database_name):
    connection = sqlite3.connect(database_name)
    return connection

def fetch_data_from_table(config_values, connection):
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM mytable")
    data = cursor.fetchall()
    return data


def main():
    #init 
    offset = None
    connection = None
    config_file = 'config_checker.cfg'

    config_values = load_config(config_file)

    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    database_name = config_values['database_name']
    table_prefix_msg = config_values['table_prefix_msg']
    table_prefix_user = config_values['table_prefix_user']
    
    
    #create db
    config_values['connection']=connect_to_database(config_values['database_name'])


    #get updates and proccess
    while True:
        updates = get_updates(config_values, offset)
        if 'result' in updates:
            for update in updates['result']:
                process_update(config_values, update)
                offset = update['update_id'] + 1
        

if __name__ == '__main__':
    main()

