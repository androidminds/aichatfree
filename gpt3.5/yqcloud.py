# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import requests
import time
from fake_useragent import UserAgent

def completion(messages, proxies=None):
    url = 'https://api.aichatos.cloud/api/generateStream'

    user_agent = UserAgent().random
    headers = {
        'authority': 'api.aichatos.cloud',
        'origin': 'https://chat9.yqcloud.top',
        'referer': 'https://chat9.yqcloud.top/',
        'user-agent': user_agent,
    }

    data = {
        'prompt': messages,
        'userId': f'#/chat/{int(time.time() * 1000)}',
        'network': True,
        'apikey': '',
        'system': '',
        'withoutContext': True,
    }
    
    return requests.post(url, headers=headers, json=data, timeout=10, proxies=proxies, stream=True)