# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from slackudf import send_msg, cat_token
import time

@on_command(['!테스트'])
def run(robot, channel, tokens, user):
    ''''''
    send_msg(robot, channel, str(channel))
    return channel, ''
