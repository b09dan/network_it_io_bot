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

#save-load bot's database
def save_data_to_file(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file)

def load_data_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        return {}

#work with user
def user_add(userid, message_hash, user_data):
    if userid not in user_data:
        user_data[userid] = []
        user_data[userid].append(userid)
        user_data[userid].append(message_hash) 
    return True

def user_whitelist_check():
#do check against whitelist and active list
    return True

#work with message: make spam decision
def message_check():
#check message against rules
    return False

#work with update
def send_message(api_url, chat_id, text, reply_to_message_id=None):
    url = f'{api_url}/sendMessage'
    params = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': reply_to_message_id}
    response = requests.post(url, params)
    return response.json()

def process_update(api_url, update, user_data):
    print(update)
    if 'message' in update and 'chat' in update['message'] and 'id' in update['message']['chat']:
        chat_id = update['message']['chat']['id']
        if 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            userid = update['message']['from']['id']

            user_add(userid, hash(message_text), user_data)

            send_message(api_url, chat_id, f'You said: {message_text}/nYour userid: {userid}', reply_to_message_id=message_id)

def get_updates(api_url, offset=None):
    url = f'{api_url}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params)
    return response.json()

def connect_to_database():
    connection = sqlite3.connect("mydatabase.db")
    return connection

def fetch_data_from_table(connection):
    cursor = connection.cursor()
#cursor.execute('''CREATE TABLE IF NOT EXISTS messages
#                  (id INTEGER PRIMARY KEY, chat_id INTEGER, message_id INTEGER, deleted INTEGER)''')

    cursor.execute("SELECT * FROM mytable")
    data = cursor.fetchall()
    return data


def main():
    connection = None
    config_file = 'config_checker.cfg'
    config_values = load_config(config_file)
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    offset = None
    user_data = load_data_from_file(config_values['database_file'])

    connection = connect_to_database()
    result = fetch_data_from_table(connection)

    while True:
        updates = get_updates(api_url, offset)
        if 'result' in updates:
            for update in updates['result']:
                process_update(api_url, update, user_data)
                offset = update['update_id'] + 1

        #save pereodically user data
        if offset and offset % 2 == 0:
            save_data_to_file(user_data, config_values['database_file'])

    if connection:
        connection.close()            

if __name__ == '__main__':
    main()

