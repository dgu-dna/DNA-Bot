# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from slackutils import cat_token, get_nickname
import time


@on_command(['!알람', '!ㅇㄹ'])
def run(robot, channel, tokens, user):
    '''일정시간 이후에 알람 울려줌'''
    msg = '사용법 오류'
    if len(tokens) > 1:
        userName = get_nickname(user)
        time.sleep(int(tokens[0]))
        msg = userName + ', ' + cat_token(tokens, 1)
    return channel, msg
