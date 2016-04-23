# -*- encoding: utf-8 -*-
import urllib, json, imp
settings = imp.load_source('settings','./settings.py')
WEB_API_TOKEN = settings.WEB_API_TOKEN
BOT_NAME = settings.BOT_NAME
ICON_URL = settings.ICON_URL

def send_msg(robot, channel, message):
	robot.client.api_call('chat.postMessage',username=BOT_NAME, as_user='false',icon_url=ICON_URL,channel=channel,text=message)

def cat_token(tokens, prefix):
    fulltok=''
    if(len(tokens) <= prefix):
        return ''
    itertok=iter(tokens)
    for i in range(prefix):
        next(itertok)
    for token in itertok:
        fulltok += token + ' '
    return fulltok[:-1]

def insert_dot(msg):
    return msg[:1] + '·' + msg[1:]

def get_nickname(user):
    url = 'https://slack.com/api/users.info?token='+WEB_API_TOKEN+'&user='+str(user)+'&pretty=1'
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return str(data['user']['name'])
