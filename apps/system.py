# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
import subprocess
import sys
import os
from subprocess import check_output
import imp
settings = imp.load_source('settings','./settings.py')
BOT_NAME = settings.BOT_NAME
ICON_URL = settings.ICON_URL
#from settings import BOT_NAME, ICON_URL

def send_msg(robot, channel, txt):
    robot.client.api_call('chat.postMessage',username=BOT_NAME+' 매니저', as_user='false',icon_url=ICON_URL,channel=channel,text=txt)

@on_command(['$'])
def run(robot, channel, tokens, user):
    ''' '''
    rootuser = set(['U0SPF91EE', 'U0SPXF0Q7'])
    if len(tokens) < 1:
        send_msg(robot, channel, '...')
        sys.exit()
    if str(user) not in rootuser:
        send_msg(robot, channel, 'Permission denied')
        sys.exit()
    if str(tokens[0]) == 'reboot':
        if len(tokens) > 1 and str(tokens[1]) == 'manager':
            file=open('booting_mgr','w')
            file.write(str(channel))
            file.close()
            send_msg(robot, channel, '승규 매니저를 재시작 합니다...')
            subprocess.call(['./reboot_mgr.sh'])
        else:
            file=open('booting','w')
            file.write(str(channel))
            file.close()
            send_msg(robot, channel, '승규를 재시작 합니다...')
            subprocess.call(['./reboot.sh'])
        sys.exit()
    if str(tokens[0]) == 'boot':
        file=open('booting','w')
        file.write(str(channel))
        file.close()
        send_msg(robot, channel, '승규를 시작합니다...')
        subprocess.call(['./run.sh'])
        sys.exit()
    if str(tokens[0]) == 'kill':
        send_msg(robot, channel, '승규를 잠재웁니다...')
        subprocess.call(['./kill_nohup.sh'])
        sys.exit()
    if str(tokens[0]) == 'debug':
        #if len(tokens) > 1 and tokens[1] == 'debug' :
        #    subprocess.call(['./reboot.sh','debug'])
        if len(tokens) > 1:
            if str(tokens[1]) == 'on':
                send_msg(robot, channel, '승규를 디버깅합니다...')
                file=open('DEBUG','w')
                file.write(str(channel))
                file.close()
            if str(tokens[1]) == 'off':
                send_msg(robot, channel, '승규 디버깅을 그만둡니다...')
                file=open('DEBUG_','w')
                file.close()
        sys.exit()
    if str(tokens[0]) == 'git':
        if str(tokens[1]) == 'pull':
            send_msg(robot, channel, check_output(['./git_pull.sh']))
            sys.exit()
        elif str(tokens[1]) == 'push':
            send_msg(robot, channel, check_output(['./git_push.sh', tokens[2]]))
            sys.exit()
        elif str(tokens[1]) == 'status':
            send_msg(robot, channel, check_output(['git', 'status']))
            sys.exit()
    sys.exit()
