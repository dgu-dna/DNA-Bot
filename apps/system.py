# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
import subprocess
from subprocess import check_output
from settings import BOT_NAME, ICON_URL

@on_command(['$'])
def run(robot, channel, tokens, user):
    ''' '''
    rootuser = set(['U0SPF91EE', 'U0SPXF0Q7'])
    if len(tokens) < 1:
        return channel, '...'
    if str(user) not in rootuser:
        return channel, 'Permission denied'
    if str(tokens[0]) == 'reboot':
        file=open('rebooting','w')
        file.write(str(channel))
        file.close()
        #robot.client.rtm_send_message(channel,'It will be reboot soon...')
	robot.client.api_call('chat.postMessage',username=BOT_NAME, as_user='false',icon_url=ICON_URL,channel=channel,text='It will be reboot soon...')
        subprocess.call(['./reboot.sh'])
        return channel, 'Rebooting...'
    if str(tokens[0]) == 'git':
        if str(tokens[1]) == 'pull':
            return channel, check_output(['./git_pull.sh'])
        elif str(tokens[1]) == 'push':
            return channel, check_output(['./git_push.sh', tokens[2]])
        elif str(tokens[1]) == 'status':
            return channel, check_output(['git', 'status'])

    return channel, '...'
