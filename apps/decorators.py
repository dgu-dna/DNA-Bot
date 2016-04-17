# coding: utf-8
from __future__ import unicode_literals

import re
import traceback
from functools import wraps
import imp

settings = imp.load_source('settings', './settings.py')
BOT_NAME = settings.BOT_NAME
ICON_URL = settings.ICON_URL
#from settings import BOT_NAME, ICON_URL

TOKENIZE_PATTERN = re.compile(r'["“](.+?)["”]|(\S+)', re.U | re.S)


def _extract_tokens(message):
    '''Parse the given message, extract command and split'em into tokens

        Args:
            message (str): user gave message

        Returns:
            (list): tokens
    '''
    return filter(lambda x: x and x.strip(), TOKENIZE_PATTERN.split(message))


def on_command(commands):
    def decorator(func):
        func.commands = commands

        @wraps(func)
        def _decorator(*args, **kwargs):
            robot, channel, message, user = args
            if commands:
                tokens = _extract_tokens(message)
                try:
                    channel, message = func(robot, channel, tokens, user)
                    if channel:
#                        robot.client.rtm_send_message(channel, message)
			robot.client.api_call('chat.postMessage',username=BOT_NAME, as_user='false',icon_url=ICON_URL,channel=channel,text=message)
                        return message
                    else:
                        print "[Warn] Couldn't delivered a message"
                except:
                    print "[Error] Couldn't delivered the message"
                    traceback.print_exc()
                    print
                    return None
            return ''
        return _decorator
    return decorator
