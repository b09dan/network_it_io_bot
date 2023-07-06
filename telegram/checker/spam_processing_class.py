import requests

class SpamProcessing:

    #start here and decide how to deal with message according to config
    def spam_main_func(config_values, chat_id, message_id, to_chat_id=None, reply_to_message_id=None):
        logger = config_values['logger']
        #forward, delete, tag_admins
        spam_processing = config_values['spam_processing']

        if spam_processing == 'delete':
            SpamProcessing.delete_message(config_values, chat_id, message_id)

        elif spam_processing == 'tag_admins':
            SpamProcessing.tag_admins(config_values, chat_id, message_id)

        else:
            logger.info('Config spam_processing is not set or unknown. Nothing to do, ignore spam.')        
        
        return True
    
    #delete message
    def delete_message(config_values, chat_id, message_id):
        logging = config_values['logger']
        bot_token =  config_values['bot_token']

        url = f"https://api.telegram.org/bot{bot_token}/deleteMessage"
        params = {
            'chat_id': chat_id,
            'message_id': message_id
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            logging.info("Succesful! Spam message was DELETED! Message_id:%s", message_id)
        else:
            logging.info("Error! Spam message was NOT DELETED! Message_id:%s", message_id)

    def tag_admins(config_values, chat_id, message_id):
        logging = config_values['logger']
        bot_token =  config_values['bot_token']
        #get admins list
        url = f"https://api.telegram.org/bot{bot_token}/getChatAdministrators?chat_id={chat_id}"
        response = requests.get(url)
        tag_admins_text = config_values['tag_admins_text']

        if response.status_code == 200:
            data = response.json()
            admins = []

            for admin in data['result']:
                user = admin['user']
                if 'username' in user:
                    admins.append(user['username'])

            tagged_admins = ' '.join(f"@{admin}" for admin in admins)
            tagged_message_text = f"{tagged_admins} {tag_admins_text}"
            SpamProcessing.send_message(config_values, chat_id, tagged_message_text, message_id)
        else:
            logging.info("Ошибка запроса: %s, %s", str(response.status_code), response.text) 

        return True       

    #auxiliary function. might be usefull for additional logs or notifications
    def send_message(config_values, chat_id, text, reply_to_message_id=None):
        logging = config_values['logger']
        bot_token =  config_values['bot_token']
        api_url = f'https://api.telegram.org/bot{bot_token}'
        url = f'{api_url}/sendMessage'
        
        params = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': reply_to_message_id}
        response = requests.post(url, params)

        if response.status_code == 200:
            logging.info("Message_id: %s. Administrators notified.", reply_to_message_id)
        else:
            logging.info("Ошибка запроса: %s, %s", str(response.status_code), response.text) 

        return True   
        return response.json()

    #auxiliary function. might be usefull for additional logs or notifications
    def forward_message(config_values, to_chat_id, from_chat_id, message_id):
        logging = config_values['logger']
        bot_token =  config_values['bot_token']

        url = f"https://api.telegram.org/bot{bot_token}/forwardMessage"
        data = {
            'chat_id': to_chat_id,
            'from_chat_id': from_chat_id,
            'message_id': message_id
        }
        response = requests.post(url, json=data)
        if response.status_code == 200:
            logging.info("Spam message was detected and forwarded. Message_id:%s", message_id)
            return True
        else:
            logging.info("Error while forwarding the message.")
            return False



