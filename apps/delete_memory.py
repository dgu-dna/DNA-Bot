#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from time import localtime, strftime
import json
import urllib
import os
from subprocess import check_output


@on_command(['!기억삭제', '!ㄱㅇㅅㅈ', '!rdtw'])
def run(robot, channel, tokens, user):
    if len(tokens) == 1:
        path = '/home/simneol/hongmoa/apps/name_cache/'+str(tokens[0])
        msg = ''
        if os.path.isfile(path):
            os.remove(path)
            msg = '이제 \''+str(tokens[0])+'\'에 대해선 몰라요! :smile_cat:'
        else:
            msg = str(tokens[0])+'(이)요? 기억할 내용이 없는 걸요ㅠ_ㅠ'
        return channel, msg
    else:
        msg = '!기억삭제, ㄱㅇㅅㅈ, rdtw\n!기억삭제 <삭제할 단어>\nex) !기억삭제 악몽'
    return channel, msg
