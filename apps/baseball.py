# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from decorators import on_command
import random

#@on_command(['테스팅'])
def run(robot, channel, tokens, user):
    '''디버깅용 기능입니다'''
    msg = ' '
    msg += str(user)
    return channel, msg

if "__main__" == __name__:
    n = []
    for i in range(3):
        while True:
            num = random.randrange(0,10)
            if num not in n:
                n.append(num)
                break
    print n
