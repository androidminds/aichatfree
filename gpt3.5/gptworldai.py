# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import requests
import random
import uuid
import binascii
import json
from Crypto.Cipher import AES
from fake_useragent import UserAgent

def __pad_data(data: bytes) -> bytes:
    block_size = AES.block_size
    padding_size = block_size - len(data) % block_size
    padding = bytes([padding_size] * padding_size)
    return data + padding

def random_token(e):
    token = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    n = len(token)
    return "".join([token[random.randint(0, n - 1)] for i in range(e)])

def encrypt(e):
    t = random_token(16).encode('utf-8')
    n = random_token(16).encode('utf-8')
    r = e.encode('utf-8')
    cipher = AES.new(t, AES.MODE_CBC, n)
    ciphertext = cipher.encrypt(__pad_data(r))
    return binascii.hexlify(ciphertext).decode('utf-8') + t.decode('utf-8') + n.decode('utf-8')


def handle_data(trunk):
    datas = trunk.decode('utf-8').split('data: ')
    content = ""
    for data in datas:
        if not data or "[DONE]" in data or not "content" in data:
            continue
        data_json = json.loads(data)
        if 'content' in data_json['choices'][0]['delta']:
            content += data_json['choices'][0]['delta'].get('content')

  
    return content.encode('utf-8')
    
def completion(messages, proxy=None):

        url = "https://chat.getgpt.world/api/chat/stream"

        headers = {
            "Content-Type": "application/json",
            "Referer": "https://chat.getgpt.world/",
            'user-agent': UserAgent().random,
        }

        data = json.dumps({
            "messages": json.loads(messages),
            "frequency_penalty": 0,
            "max_tokens": 4000,
            "model": "gpt-3.5-turbo",
            "presence_penalty": 0,
            "temperature": 1,
            "top_p": 1,
            "stream": True,
            "uuid": str(uuid.uuid4())
        })
        data = json.dumps({"signature": encrypt(data)})

        timeout = 10 # 设置超时时间为10秒
        proxies = {'http': proxy, 'https': proxy} if proxy else None       

        try:
            return requests.post(url, headers=headers, data=data, timeout=timeout, proxies=proxies, stream=True)    
        except Exception as e:
            print("Gptworldai post error: ", e)
            return None
        