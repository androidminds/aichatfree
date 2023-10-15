# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import requests
import json

def completion(messages, **kwargs):
    url = "https://chatgpt4online.org/wp-json/mwai-ui/v1/chats/submit"
    data = {
        "botId": "default",
        "customId": None,
        "session": "N/A",
        "chatId": "",
        "contextId": 58,
        "messages": messages,
        "newMessage": messages[-1]["content"],
        "stream": True
    }
    proxies = kwargs.get("proxies", None)
   
    try: 
        response = requests.post(url, json=data, proxies=proxies, stream=True)
        response.raise_for_status()
    except Exception as e:
        yield str(e)
        return
    
    for line in response.iter_lines():
        if line.startswith(b"data: "):
            line = json.loads(line[6:])
            if line["type"] == "live":
                yield line["data"]