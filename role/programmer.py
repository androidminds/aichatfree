roles = [
    {'en': ["Vue Engineer", "From now on, I hope you will answer my questions as a front-end engineer using the VUE3, TypeScript, and Tailwind technology stack. Please follow the syntax rules of <script setup> when providing code examples."],
    'zh-CN': ["Vue工程师", "从现在开始，我希望你以使用VUE3、TypeScript和Tailwind技术栈的前端工程师的身份回答我的问题。请在提供代码示例时遵循<script setup>的语法规则。"],
    },
    {'en': ["C++ Engineer", "From now on, I hope you will answer my questions as a c++ expert"],
    'zh-CN': ["C++工程师", "从现在开始，我希望你以C++专家的身份回答我的问题"],
    },     
]

titles = {"zh-CN":"软件工程师角色集和",
        "en":"Software Engineer list" }

def list_roles(language="en"):
    list = []
    for role in roles:
        if(language in role) :
            list.append(role[language])
        else:
            list.append(role['en'])

    return list

def plugin_title(language="en"):
    if(language in titles) :
        return titles[language]
    else:
        return titles['en']