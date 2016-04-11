#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
import subprocess
@on_command(['REBOOT'])
def run(robot, channel, tokens, user):
    ''' 일반 사용자는 이용할 수 없습니다'''
    rootuser=set(['U0SPF91EE','U0SPXF0Q7'])
    if str(user) not in rootuser:
        return channel, '일반 사용자는 이용할 수 없습니다'
    subprocess.call(["/home/simneol/hongmoa/reboot.sh"])
    return channel, 'REBOOTING...'
