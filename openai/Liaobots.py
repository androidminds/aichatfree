# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import uuid
import requests
import json
models = {
    "gpt-4": {
        "id": "gpt-4",
        "name": "GPT-4",
        "maxLength": 24000,
        "tokenLimit": 8000,
    },
    "gpt-3.5-turbo": {
        "id": "gpt-3.5-turbo",
        "name": "GPT-3.5",
        "maxLength": 12000,
        "tokenLimit": 4000,
    },
    "gpt-3.5-turbo-16k": {
        "id": "gpt-3.5-turbo-16k",
        "name": "GPT-3.5-16k",
        "maxLength": 48000,
        "tokenLimit": 16000,
    },
}


def completion(messages, **kwargs):
    model = kwargs.get('model', "gpt-3.5-turbo")
    url = "https://liaobots.site"
    model = model if model in models else "gpt-3.5-turbo"
    headers = {
        "authority": "liaobots.com",
        "content-type": "application/json",
        "origin": url,
        "referer": url + "/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    }
    proxies = kwargs.get("proxies", None)

    response = requests.post("https://liaobots.work/recaptcha/api/login", 
                             headers=headers, 
                             data={"token": "abcdefghijklmnopqrst"}, 
                             proxies = proxies, 
                             verify = False)
    response.raise_for_status()
    response = requests.post(
            "https://liaobots.work/api/user",
            proxies = proxies,
            headers=headers, 
            json={"authcode": ""},
            verify=False)
    response.raise_for_status()
    data = response.json()
    _auth_code = data.get("authCode")
    data = {
        "conversationId": str(uuid.uuid4()),
        "model": models[model],
        "messages": messages,
        "key": "",
        "prompt": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully.",
    }
    requests.post(
            "https://liaobots.work/api/chat",
            proxies = proxies,
            json=data,
            headers={"x-auth-code": _auth_code},
            verify=False
        )
    response.raise_for_status()
    for stream in response.content.iter_any():
        if stream:
            yield stream.decode()



