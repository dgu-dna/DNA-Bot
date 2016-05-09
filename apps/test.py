# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command


@on_command(['테스팅'])
def run(robot, channel, tokens, user):
    '''디버깅용 기능입니다'''
    msg = ' '
    msg += str(user)
    return channel, msg
