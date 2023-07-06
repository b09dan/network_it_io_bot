import requests

def class SpamProcessing:
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

    def forward_message(config_values, to_chat_id, from_chat_id, message_id):
        bot_token =  config_values['bot_token']
        #TODO: remove or cnahge. development mode
        to_chat_id = config_values['chat_reply_restrict']

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


