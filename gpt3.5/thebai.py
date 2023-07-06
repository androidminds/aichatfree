# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 

import requests
import json
from fake_useragent import UserAgent


def handle_data(trunk):
    datas = trunk.decode('utf-8').split('\n')
    content = ""
    for data in datas:
        if len(data) > 0:
            data_json = json.loads(data)
            if 'delta' in data_json:
                content += data_json['delta']
            
    return content.encode('utf-8')
    

def completion(messages, proxy=None):  
    url = 'https://chatbot.theb.ai/api/chat-process'

    headers = {
        'Content-Type': 'application/json',
        'Origin': 'https://chatbot.theb.ai',
        'Referer': 'https://chatbot.theb.ai/',
        'User-Agent': UserAgent().random,
    }

    payload = {
        "prompt": messages,
        "options": {},
    }
        
    timeout = 10 
    proxies = {'http': proxy, 'https': proxy} if proxy else None

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=timeout, proxies=proxies, stream=True)
        response.raise_for_status()           
        return response
    except (requests.exceptions.RequestException) as e:
        print("thebai Post error: ", e)
        return None
        