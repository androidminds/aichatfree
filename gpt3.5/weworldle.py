# Copyright Notice:
# This file has been modified and supplemented based on the xtekky/gpt4free.
# The copyright belongs to the original project and its developers. 
# Thanks to the original project and its developers.
# 
import json
import requests, random, string, time
from typing  import Any

def handle_data(data):
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"]
    else:
        return data

def completion(messages, proxies=None):
    url = "https://wewordle.org/gptapi/v1/android/turbo"
        
    messages = json.loads(messages)

    # randomize user id and app id
    _user_id = "".join(
        random.choices(f"{string.ascii_lowercase}{string.digits}", k=16))
    
    _app_id = "".join(
        random.choices(f"{string.ascii_lowercase}{string.digits}", k=31))
    
    # make current date with format utc
    _request_date = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    headers = {
        "accept"        : "*/*",
        "pragma"        : "no-cache",
        "Content-Type"  : "application/json",
        "Connection"    : "keep-alive"
        # user agent android client
        # 'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 10; SM-G975F Build/QP1A.190711.020)',
    }
    
    data: dict[str, Any] = {
        "user"      : _user_id,
        "messages"  : messages,
        "subscriber": {
            "originalPurchaseDate"          : None,
            "originalApplicationVersion"    : None,
            "allPurchaseDatesMillis"        : {},
            "entitlements"                  : {"active": {}, "all": {}},
            "allPurchaseDates"              : {},
            "allExpirationDatesMillis"      : {},
            "allExpirationDates"            : {},
            "originalAppUserId"             : f"$RCAnonymousID:{_app_id}",
            "latestExpirationDate"          : None,
            "requestDate"                   : _request_date,
            "latestExpirationDateMillis"    : None,
            "nonSubscriptionTransactions"   : [],
            "originalPurchaseDateMillis"    : None,
            "managementURL"                 : None,
            "allPurchasedProductIdentifiers": [],
            "firstSeen"                     : _request_date,
            "activeSubscriptions"           : [],
        }
    }    

    return requests.post(url, headers=headers, json=json.dumps(data), timeout=10, proxies=proxies, stream=False)

