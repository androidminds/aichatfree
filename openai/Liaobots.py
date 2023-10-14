# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import uuid
from aiohttp import ClientSession

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


async def completion(messages, **kwargs):
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
    async with ClientSession(
        headers=headers
    ) as session:

        async with session.post(
            "https://liaobots.work/recaptcha/api/login",
            proxy=proxies,
            data={"token": "abcdefghijklmnopqrst"},
            verify_ssl=False
        ) as response:
            response.raise_for_status()
        async with session.post(
            "https://liaobots.work/api/user",
            proxy=proxies,
            json={"authcode": ""},
            verify_ssl=False
        ) as response:
            response.raise_for_status()
            _auth_code = (await response.json(content_type=None))["authCode"]
        data = {
            "conversationId": str(uuid.uuid4()),
            "model": models[model],
            "messages": messages,
            "key": "",
            "prompt": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully.",
        }
        async with session.post(
            "https://liaobots.work/api/chat",
            proxy=proxies,
            json=data,
            headers={"x-auth-code": _auth_code},
            verify_ssl=False
        ) as response:
            response.raise_for_status()
            async for stream in response.content.iter_any():
                if stream:
                    yield stream.decode()



