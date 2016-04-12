#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
import subprocess
from subprocess import check_output
@on_command(['SYSTEM'])
def run(robot, channel, tokens, user):
    ''' 일반 사용자는 이용할 수 없습니다'''
    rootuser=set(['U0SPF91EE','U0SPXF0Q7'])
    if str(user) not in rootuser:
        return channel, 'Permission denied'
    if len(tokens) < 1:
        return channel, 'need arguments'
    if str(tokens[0]) == 'REBOOT':
        subprocess.call(['/home/simneol/hongmoa/reboot.sh'])
        return channel, 'Rebooting...'
    elif str(tokens[0]) == 'PULL':
        #subprocess.call(['/home/simneol/hongmoa/git_pull.sh'])
        return channel, check_output(['/home/simneol/hongmoa/git_pull.sh'])
    elif str(tokens[0]) == 'PUSH':
        arg = ''
        for token in tokens:
            arg+=str(token)+' '
        arg = arg[4:-1]
        #subprocess.call(['/home/simneol/hongmoa/git_push.sh',arg])
        return channel, check_output(['/home/simneol/hongmoa/git_push.sh',arg])

    return channel, '...'
