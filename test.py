import json
import importlib
import requests
from pathlib import Path
import asyncio
import sys
from asyncio import AbstractEventLoop

def load_plugin(path):
    try:
        spec = importlib.util.spec_from_file_location("module_name", Path(path))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        if hasattr(module, "completion") and callable(module.completion):
            completion = module.completion
        else:
            completion = None

        return completion
    except Exception as e:
        print("load_plugin:", e)
        return None
    
    
async def anext(async_iterable):
    try:
        return await async_iterable.__anext__()
    except StopAsyncIteration:
        raise StopAsyncIteration
    
async def plugin_completion(file):

    completion = load_plugin(file)

    if completion is None:
        raise Exception(f"Missing completion function in plugin {file}")

    generator = completion(messages=[{"role": "user", "content": "Hello, who are you?"}]) 

    async for value in generator:
        print(value)
        
        try:
            next_value = await anext(generator)
        except StopAsyncIteration:
            break;
        
        print(next_value)


def TestAll():
    plugins = [
        "./openai/Aivvm.py", 
        "./openai/ChatAiGpt.py", 
        "./openai/Chatgpt4Online.py", 
        "./openai/GetGpt.py", 
        "./openai/Liaobots.py", 
        "./openai/yqcloud.py"]
    result=[]
    for file in plugins:
        try:
            asyncio.run(plugin_completion(file))
        except:
            result.append(file)

    print("Following plugin cannot connected:")
    print(result)

def TestOne():
    asyncio.run(plugin_completion("./openai/Aivvm.py"))

TestOne()
