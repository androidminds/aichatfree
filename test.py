
import importlib
from pathlib import Path
import asyncio


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
            completion = load_plugin(file)
            if completion is None:
                raise Exception(f"Missing completion function in plugin ")

            generator = completion(messages=[{"role": "user", "content": "Hello, who are you?"}]) 

            for result in generator:
                print(result)

        except:
            result.append(file)

    print("Following plugin cannot connected:")
    print(result)

def TestOne():
    completion = load_plugin("./openai/Aivvm.py")

    if completion is None:
        raise Exception(f"Missing completion function in plugin ")

    generator = completion(messages=[{"role": "user", "content": "Hello, who are you?"}]) 

    for result in generator:
        print(result)
        
TestOne()

