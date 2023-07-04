import requests
import json
import logging
from rules_class import Rules
from db_functions_class import DbFunctions
from training_class import Training

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
        is_spam = 0
        chat_id = update['message']['chat']['id']
        #TODO: dont forget to think about the whitelist   and chat_id in config_values['chat_whitelist']
        if 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            user_id = update['message']['from']['id']

            is_spam = int(Rules.message_check(config_values, message_text, user_id, 0, 0))

            DbFunctions.save_user(config_values, message_text, user_id, message_id, chat_id)
            DbFunctions.save_message(config_values, message_text, user_id, message_id, chat_id, is_spam)       
            
            logging.debug("Update processed. Chat_id=%s Message_id=%s User_id=%s", chat_id, message_id, user_id)
            #TODO: do not send message here, it's only for tests
            #send_message(config_values, chat_id, f'You said: {message_text}\nYour userid: {user_id}', reply_to_message_id=message_id)

def get_updates(config_values, offset=None):
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    url = f'{api_url}/getUpdates'

    params = {'offset': offset}
    response = requests.get(url, params)
    return response.json()



def main():
    #init 
    offset = None
    connection = None
    config_file = 'config_checker.cfg'

    config_values = load_config(config_file)

    #TODO: add setting log level
    #log_level = config_values['loglevel']
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    #create db and db connection
    config_values['connection']=DbFunctions.connect_to_database(config_values['database_name'])

    if config_values['mode'] == "general":
        #get updates and proccess them
        while True:
            updates = get_updates(config_values, offset)
            if 'result' in updates:
                for update in updates['result']:
                    process_update(config_values, update)
                    offset = update['update_id'] + 1
    elif config_values['mode'] == "training":
            Training.train_good(config_values)
            print("----------------")
            Training.train_bad(config_values)

if __name__ == '__main__':
    main()

