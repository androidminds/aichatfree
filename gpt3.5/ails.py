# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import time
import json
import uuid
import hashlib
import requests

from typing import NewType, Dict
from datetime import datetime
sha256 = NewType('sha_256_hash', str)

def hash(json_data: Dict[str, str]) -> sha256:
    base_string: str = '%s:%s:%s:%s' % (
        json_data['t'],
        json_data['m'],
        'WI,2rU#_r:r~aF4aJ36[.Z(/8Rv93Rf',
        len(json_data['m'])
    )
    return hashlib.sha256(base_string.encode()).hexdigest()

def format_timestamp(timestamp: int) -> str:
    e = timestamp
    n = e % 10
    r = n + 1 if n % 2 == 0 else n
    return str(e - n + r)
    
def handle_data(trunk):
    datas = trunk.decode('utf-8').split('data: ')
    content = ""
    for data in datas:
        if not data or "[DONE]" in data or not "content" in data:
            continue
        data_json = json.loads(data)
        if 'content' in data_json['choices'][0]['delta']:
            content += data_json['choices'][0]['delta'].get('content')

    return content.encode('utf-8')


def completion(messages, proxy=None):
    url = 'https://api.caipacity.com/v1/chat/completions'

    messages = json.loads(messages)
    headers = {
        'authority': 'api.caipacity.com',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'authorization': 'Bearer free',
        'client-id': str(uuid.uuid4()),
        'client-v': '0.1.249',
        'content-type': 'application/json',
        'origin': 'https://ai.ls',
        'referer': 'https://ai.ls/',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

    timestamp = format_timestamp(int(time.time() * 1000))

    sig = {
        'd': datetime.now().strftime('%Y-%m-%d'),
        't': timestamp,
        's': hash({
            't': timestamp,
            'm': messages[-1]['content']})}

    data = json.dumps(separators=(',', ':'), obj= {
        'model': 'gpt-3.5-turbo',
        'temperature': 0.6,
        'stream': True,
         'messages': messages} | sig)

    timeout = 10
    proxies = {'http': proxy, 'https': proxy} if proxy else None       

    try:
        return requests.post(url, headers=headers, data=data, timeout=timeout, proxies=proxies, stream=True), True
    except Exception as e:
        print("ails post error: ", e)
        return None, False
