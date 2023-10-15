# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 

import re
import requests
from json import dumps, loads

def completion(messages, **kwargs):
    url = "https://chataigpt.org"

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
        "Accept": "*/*",
        "Accept-Language": "de,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Origin": url,
        "Alt-Used": url,
        "Connection": "keep-alive",
        "Referer": url,
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "TE": "trailers",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
    }

    proxies = kwargs.get("proxies", None)

    response = requests.get(f"{url}/", headers=headers, proxies=proxies)
    response.raise_for_status()
    response = response.text
    result = re.search(r'data-nonce=(.*?) data-post-id=([0-9]+)', response)
    if not result:
        raise RuntimeError("No nonce found")
    _nonce, _post_id = result.group(1), result.group(2)


    prompt = dumps(messages)
    data = {
        "_wpnonce": _nonce,
        "post_id": _post_id,
        "url": url,
        "action": "wpaicg_chat_shortcode_message",
        "message": prompt,
        "bot_id": 0
    }

    response = requests.post(f"{url}/wp-admin/admin-ajax.php", headers=headers, data=data, proxies=proxies, stream=True)
    response.raise_for_status()
    for chunk in response.iter_content(chunk_size=4096):
        if chunk:
            data = chunk.decode()
            data = loads(data)
            if "data" in data :
                string = data["data"].replace("\\", "")
                data = loads(string)
                yield data[0]["content"]