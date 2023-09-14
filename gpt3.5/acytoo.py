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

def completion(messages, proxy=None):
    url = 'https://chat.acytoo.com/api/completions'

    messages = json.loads(messages)

    headers = {
        'accept': '*/*',
        'content-type': 'application/json',   }

    timeout = 10
    proxies = {'http': proxy, 'https': proxy} if proxy else None       

    try:
        return requests.post(url, headers=headers, json=_create_payload(messages), timeout=timeout, proxies=proxies, stream=False), False
    except Exception as e:
        print("acytoo post error: ", e)
        return None, False