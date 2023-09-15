import time
import json
import requests

def _create_payload(messages: list[dict[str, str]]):
    payload_messages = [
        message | {'createdAt': int(time.time()) * 1000} for message in messages
    ]
    
    return {
        'key'         : '',
        'model'       : 'gpt-3.5-turbo',
        'messages'    : payload_messages,
        'temperature' : 1,
        'password'    : ''
    }

def completion(messages, proxies=None):
    url = 'https://chat.acytoo.com/api/completions'

    messages = json.loads(messages)

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',   }
 

    requests.post(url, headers=headers, json=_create_payload(messages), timeout=10, proxies=proxies, stream=False)