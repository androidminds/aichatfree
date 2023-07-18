# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import requests
import random
import hashlib
import json
from fake_useragent import UserAgent

def md5(text):
    return hashlib.md5(text.encode()).hexdigest()[::-1]

def get_api_key(user_agent):
    part1 = str(random.randint(0, 10**11))
    part2 = md5(user_agent + md5(user_agent + md5(user_agent+part1+"x")))
    return f"tryit-{part1}-{part2}"

def completion(messages, proxy=None):
    url = "https://api.deepai.org/chat_response"

    user_agent = UserAgent().random
    headers = {
        "user-agent": user_agent,
        "api-key": get_api_key(user_agent)
    }

    files = {
        "chat_style": (None, "chat"),
        "chatHistory": (None, messages)
    }

    timeout = 10
    proxies = {'http': proxy, 'https': proxy} if proxy else None       

    try:
        return requests.post(url, headers=headers, files=files, timeout=timeout, proxies=proxies, stream=True)
    except Exception as e:
        print("DeepAI post error: ", e)
        return None