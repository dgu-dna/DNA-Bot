# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import cat_token, get_nickname, send_msg
import time


@on_command(['!알람', '!ㅇㄹ'])
def run(robot, channel, tokens, user, command):
    '''일정시간 이후에 알람 울려줌'''
    msg = '사용법 오류'
    if len(tokens) > 1:
        user_name = get_nickname(user)
        sec = eval(tokens[0])
        noti_msg = user_name + ', ' + str(sec) + '초 후에 알려주겠음.'
        send_msg(robot, channel, noti_msg)
        time.sleep(sec)
        msg = '<@' + user + '>, ' + cat_token(tokens, 1)
    return channel, msg
