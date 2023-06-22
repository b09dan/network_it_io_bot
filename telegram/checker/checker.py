import requests

def load_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line and not line.startswith('#'):  # Пропускаем пустые строки и комментарии
                key, value = line.split('=')
                config[key.strip()] = value.strip()
    return config

def send_message(api_url, chat_id, text, reply_to_message_id=None):
    url = f'{api_url}/sendMessage'
    params = {'chat_id': chat_id, 'text': text, 'reply_to_message_id': reply_to_message_id}
    response = requests.post(url, params)
    return response.json()

def process_update(api_url, update):
    print(update)
    if 'message' in update and 'chat' in update['message'] and 'id' in update['message']['chat']:
        chat_id = update['message']['chat']['id']
        if 'text' in update['message']:
            message_text = update['message']['text']
            message_id = update['message']['message_id']
            send_message(api_url, chat_id, f'You said: {message_text}', reply_to_message_id=message_id)

def get_updates(api_url, offset=None):
    url = f'{api_url}/getUpdates'
    params = {'offset': offset}
    response = requests.get(url, params)
    return response.json()

def main():
    file_path = 'config_checker.cfg'
    bot_token =  load_config(file_path)['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    offset = None
    while True:
        updates = get_updates(api_url, offset)
        if 'result' in updates:
            for update in updates['result']:
                process_update(api_url, update)
                offset = update['update_id'] + 1

if __name__ == '__main__':
    main()

