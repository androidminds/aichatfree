
import json
import os
import uuid

# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 

import requests
from Crypto.Cipher import AES


async def completion(messages, **kwargs):
    
    headers = {
        'Content-Type'  : 'application/json',
        'Referer'       : 'https://chat.getgpt.world/',
        'user-agent'    : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }
    
    data = json.dumps(
        {
            'messages'          : messages,
            'frequency_penalty' : kwargs.get('frequency_penalty', 0),
            'max_tokens'        : kwargs.get('max_tokens', 4000),
            'model'             : 'gpt-3.5-turbo',
            'presence_penalty'  : kwargs.get('presence_penalty', 0),
            'temperature'       : kwargs.get('temperature', 1),
            'top_p'             : kwargs.get('top_p', 1),
            'stream'            : True,
            'uuid'              : str(uuid.uuid4())
        }
    )

    proxies = kwargs.get("proxies", None)

    res = requests.post('https://chat.getgpt.world/api/chat/stream', proxies=proxies, 
        headers=headers, json={'signature': _encrypt(data)}, stream=True)

    res.raise_for_status()
    for line in res.iter_lines():
        if b'content' in line:
            line_json = json.loads(line.decode('utf-8').split('data: ')[1])
            yield (line_json['choices'][0]['delta']['content'])


def _encrypt(e: str):
    t = os.urandom(8).hex().encode('utf-8')
    n = os.urandom(8).hex().encode('utf-8')
    r = e.encode('utf-8')
    
    cipher     = AES.new(t, AES.MODE_CBC, n)
    ciphertext = cipher.encrypt(_pad_data(r))
    
    return ciphertext.hex() + t.decode('utf-8') + n.decode('utf-8')


def _pad_data(data: bytes) -> bytes:
    block_size   = AES.block_size
    padding_size = block_size - len(data) % block_size
    padding      = bytes([padding_size] * padding_size)
    
    return data + padding
