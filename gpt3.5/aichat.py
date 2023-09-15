# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import json
import requests

def handle_data(data):
    if data['response']:
        return data["message"]
    else:
        return data

def completion(messages, proxies=None):
    url = "https://chat-gpt.org/api/text"
        
    messages = json.loads(messages)
    base = ""
    for message in messages:
        base += "%s: %s\n" % (message["role"], message["content"])
    base += "assistant:"

    headers = {
        "authority": "chat-gpt.org",
        "accept": "*/*",
        "cache-control": "no-cache",
        "content-type": "application/json",
        "origin": "https://chat-gpt.org",
        "pragma": "no-cache",
        "referer": "https://chat-gpt.org/chat",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    }

    json_data = {
        "message": base,
        "temperature": 1,
        "presence_penalty": 0,
        "top_p": 1,
        "frequency_penalty": 0,
    }
    
    return requests.post(url, headers=headers, json=json_data, timeout=10, proxies=proxies, stream=False)

