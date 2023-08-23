import datetime

import requests
import json
import logging
import logging.config
import os
from rules_class import Rules
from db_functions_class import DbFunctions
from training_class import Training
from spam_processing_class import SpamProcessing

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


#work with update. Hint: chat_whitelist helps to ignore chats.
def process_update(config_values, update):
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'

    if 'message' in update and 'chat' in update['message'] and 'id' in update['message']['chat']:
        logging.info(update)
        is_spam = 0
        chat_id = update['message']['chat']['id']
        
        #if whitelist is set, work only with whitelist
        if (config_values['chat_whitelist'] is not None or config_values['chat_whitelist'] != '') and str(chat_id) not in config_values['chat_whitelist']:
            logging.info("Ignore chat_id = %s. chat_whitelist is %s", str(chat_id), config_values['chat_whitelist'])
            return True

        if 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            user_id = update['message']['from']['id']

            is_spam = int(Rules.message_check(config_values, message_text, user_id, chat_id, 0, message_id))

            DbFunctions.save_user(config_values, message_text, user_id, message_id, chat_id, is_spam)
            DbFunctions.save_message(config_values, message_text, user_id, message_id, chat_id, is_spam)       
            
            logging.debug("Update processed. Chat_id=%s Message_id=%s User_id=%s", chat_id, message_id, user_id)
            if is_spam:
                SpamProcessing.spam_main_func(config_values, chat_id, message_id)
    return True

def get_updates(config_values, offset=None):
    logging.info("Heartbeat: %s", datetime.datetime.now())
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    url = f'{api_url}/getUpdates'

    params = {'offset': offset}
    response = requests.get(url, params)

    if response.status_code == 200:
        return response.json()
    else:
        logging.error("ERROR! Update failed with status code %s %s. Check also bot_token.", str(response.status_code), response.text)
        return None



def main():
    #init 
    offset = None
    connection = None
    config_file = 'config_checker.cfg'

    config_values = load_config(config_file)

    #set log level from log_conf_file
    logging.config.fileConfig(config_values['log_conf_file'])
    config_values['logger'] = logging.getLogger()
    
    #create db and db connection
    config_values['connection'] = DbFunctions.connect_to_database(config_values['database_name'])

    #get and rewrite bot_token if bot token is set in ENV, also unset ENV
    if 'BOT_TOKEN' in os.environ:
        config_values['bot_token'] = os.environ['BOT_TOKEN']
        #del os.environ['BOT_TOKEN']

    #delete config file and unset ENV
    #if os.path.exists(config_file):
    #    os.remove(config_file)

    if config_values['mode'] == "general":
        #get updates and proccess them
        while True:
            updates = get_updates(config_values, offset)
            if updates is not None and 'result' in updates:
                for update in updates['result']:
                    process_update(config_values, update)
                    offset = update['update_id'] + 1
            elif updates is None:
                return False

    elif config_values['mode'] == "training":
            Training.train_good(config_values)
            logging.info("----------------")
            Training.train_bad(config_values)

if __name__ == '__main__':
    main()

