import requests

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

def main():
    config_file = 'config_checker.cfg'
    config_values = load_config(config_file)
    bot_token =  config_values['bot_token']
    api_url = f'https://api.telegram.org/bot{bot_token}'
    offset = None
    user_data = load_data_from_file(config_values['database_file'])

    while True:
        updates = get_updates(api_url, offset)
        if 'result' in updates:
            for update in updates['result']:
                process_update(api_url, update)
                offset = update['update_id'] + 1

if __name__ == '__main__':
    main()

