'''

创建一个便于复用的请求头

'''
from fake_useragent import UserAgent

def fake_headers():
    user_Agent = UserAgent()
    agent = user_Agent.random
    headers = {
        "User-Agent": agent
    }
    return headers