# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import requests
import time
from fake_useragent import UserAgent
from json import dumps

def completion(messages, **kwargs):
    url = 'https://api.aichatos.cloud/api/generateStream'

    user_agent = UserAgent().random
    headers = {
        'authority': 'api.aichatos.cloud',
        'origin': 'https://chat9.yqcloud.top',
        'referer': 'https://chat9.yqcloud.top/',
        'user-agent': user_agent,
    }

    data = {
        'prompt': dumps(messages),
        'userId': f'#/chat/{int(time.time() * 1000)}',
        'network': True,
        'apikey': '',
        'system': '',
        'withoutContext': True,
    }
    proxies = kwargs.get("proxies", None)

    response = requests.post(url, headers=headers, json=data, proxies=proxies, stream=True)
    response.raise_for_status()

    for chunk in response.iter_content(chunk_size=4096):
        try:
            yield chunk.decode("utf-8")
        except UnicodeDecodeError:
            yield chunk.decode("unicode-escape")