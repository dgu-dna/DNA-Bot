# -*- encoding: utf-8 -*-
from urllib.request import urlopen, quote
from bs4 import BeautifulSoup
import json
import imp
import re


NAVER_DICTIONARY_URL = 'http://krdic.naver.com/search.nhn?query=%s&kind=keyword'
settings = imp.load_source('settings', './settings.py')
WEB_API_TOKEN = settings.WEB_API_TOKEN
BOT_NAME = settings.BOT_NAME
ICON_URL = settings.ICON_URL


def send_msg(robot, channel, message=None, attachments=None):
    if attachments == None:
        return robot.client.api_call('chat.postMessage', username=BOT_NAME, as_user='false', icon_url=ICON_URL, channel=channel, text=message)
    else:
        return robot.client.api_call('chat.postMessage', username=BOT_NAME, as_user='false', icon_url=ICON_URL, channel=channel, attachments=json.dumps(attachments))

def cat_token(tokens, prefix):
    if(len(tokens) <= prefix):
        return ''
    return ' '.join(tokens).split(' ', prefix)[prefix]

def insert_dot(msg):
    return msg[:1] + '·' + msg[1:]

def get_nickname(user):
    url = 'https://slack.com/api/users.info?token='+WEB_API_TOKEN+'&user='+str(user)+'&pretty=1'
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    return str(data['user']['name'])

def get_userinfo(user, arg):
    url = 'https://slack.com/api/users.info?token='+WEB_API_TOKEN+'&user='+str(user)+'&pretty=1'
    response = urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    if len(arg) == 1:
        return data['user'][arg[0]]
    else:
        return data['user'][arg[0]][arg[1]]

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_koreanword(word):
    is_word = False
    html = urlopen(quote((NAVER_DICTIONARY_URL % word).encode('utf-8'), '/:&?='))
    soup = BeautifulSoup(html, 'html.parser')
    s = soup.find_all('a', {'class': 'fnt15'})
    t = soup.find_all('ul', {'class': 'lst3'})
    t = t[0].find_all('li')

    del_list = []
    for idx, val in enumerate(t):
        if val.p is None:
            del_list.append(idx)
    for idx in reversed(del_list):
        del t[idx]

    if s and t:
        for ss, tt in list(zip(s, t)):
            if re.sub(r'[^가-힣]', '', str(ss)) == word and tt.p.text[1:3] == '명사':
                is_word = True
                break
    return is_word
