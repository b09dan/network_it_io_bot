import requests
import json
import sqlite3
import logging
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

    query = f'CREATE TABLE IF NOT EXISTS "{table_prefix_msg}{chat_id}" (message_id INTEGER PRIMARY KEY, user_id INTEGER, message_text TEXT, deleted INTEGER)'
    connection.execute(query)
    connection.commit()

    data = (message_id, user_id, message_text[:1000], 0)
    query = f'REPLACE INTO "{table_prefix_msg}{chat_id}" (message_id, user_id, message_text, deleted) VALUES (?, ?, ?, ?)'
    connection.execute(query, data)
    connection.commit()

    return True

#work with user
def save_user(config_values, message_text, user_id, message_id, chat_id):
    table_prefix_user = config_values['table_prefix_user']
    connection = config_values['connection']

    query = f'CREATE TABLE IF NOT EXISTS "{table_prefix_user}{chat_id}" (user_id INTEGER PRIMARY KEY, message_hash TEXT, human INTEGER, messages_count INTEGER, timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP)'
    connection.execute(query)
    connection.commit()
    
    #messages count = 0, human = 0. TODO: fix it
    data = (user_id, hash(message_text[:1000]), 0,0,)
    query = f'REPLACE INTO "{table_prefix_user}{chat_id}" (user_id, message_hash, human, messages_count) VALUES (?, ?, ?, ?)'
    connection.execute(query, data)
    connection.commit()

    return True

#work with update TODO:send message only to chat_reply_restrict chat
def send_message(config_values, chat_id, text, reply_to_message_id=None):
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    url = f'{api_url}/sendMessage'
    #TODO: think about sending to other chats, but now restrict sending only to config (avoiding unnecessary spam)
    chat_id = config_values['chat_reply_restrict']
    
    params = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': reply_to_message_id}
    response = requests.post(url, params)
    return response.json()

#TODO: read only chat_whitelist (development mode)
def process_update(config_values, update):
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'

    if 'message' in update and 'chat' in update['message'] and 'id' in update['message']['chat']:
        logging.info(update)
        chat_id = update['message']['chat']['id']
        #TODO: dont forget to think about the whitelist   and chat_id in config_values['chat_whitelist']
        if 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            user_id = update['message']['from']['id']

            save_message(config_values, message_text, user_id, message_id, chat_id)
            save_user(config_values, message_text, user_id, message_id, chat_id)

            logging.debug("Update processed. Chat_id=% Message_id=% User_id=%", chat_id, message_id, user_id)
            #TODO: do not send message here, it's only for tests
            #send_message(config_values, chat_id, f'You said: {message_text}\nYour userid: {user_id}', reply_to_message_id=message_id)

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

def main():
    #init 
    offset = None
    connection = None
    config_file = 'config_checker.cfg'

    config_values = load_config(config_file)

    #log level
    log_level = config_values['loglevel']
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    #create db and db connection
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

