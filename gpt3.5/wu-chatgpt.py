import requests
import random
import json
from fake_useragent import UserAgent


def completion(messages, proxy=None, data=None):
    user = "1685"+''.join(random.sample('0123456789', 9))

    url = "https://chat2.wuguokai.cn/api/chat-process"

    headers = {
        'Origin': 'https://chat.wuguokai.cn',
        'Referer': 'https://chat.wuguokai.cn',
        'User-Agent': UserAgent().random,
    }
    payload = {
        "prompt": messages,
        "options": {},
        "userId": "#/chat/"+ user,
        "usingContext": False
    }

    timeout = 10
    proxies = {'http': proxy, 'https': proxy} if proxy else None
        
    # for a new userId, this site will send a weclome message, so we send a null prompt to bypass it
    try:
        null_payload = {"prompt": "", "userId": "#/chat/"+ user}
        requests.post(url, headers=headers, json=null_payload, timeout=timeout, proxies=proxies, stream=False)    
    except (requests.exceptions.RequestException) as e:
        print("WuChartGPT Post error: ", e)
        return None

    # send real prompt
    try:
        return requests.post(url, headers=headers, json=payload, timeout=timeout, proxies=proxies, stream=True), True
    except Exception as e:
        print("WuChartGPT Post error: ", e)
        return None, False
        