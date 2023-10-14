# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
from aiohttp import ClientSession
import json

async def completion(messages, **kwargs):
    async with ClientSession() as session:
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
        async with session.post(url, json=data, proxy=proxies) as response:
            response.raise_for_status()
            async for line in response.content:
                if line.startswith(b"data: "):
                    line = json.loads(line[6:])
                    if line["type"] == "live":
                        yield line["data"]
