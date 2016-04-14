# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
import subprocess
from subprocess import check_output


@on_command(['$'])
def run(robot, channel, tokens, user):
    ''' '''
    rootuser = set(['U0SPF91EE', 'U0SPXF0Q7'])
    if len(tokens) < 1:
        return channel, '...'
    if str(user) not in rootuser:
        return channel, 'Permission denied'
    if str(tokens[0]) == 'reboot':
        subprocess.call(['/home/simneol/hongmoa/reboot.sh'])
        return channel, 'Rebooting...'
    if str(tokens[0]) == 'git':
        if str(tokens[1]) == 'pull':
            return channel, check_output(['/home/simneol/hongmoa/git_pull.sh'])
        elif str(tokens[1]) == 'push':
            # arg = ''
            # for token in tokens:
            #    arg+=str(token)+' '
            # arg = arg[4:-1]
            return channel, check_output(['/home/simneol/hongmoa/git_push.sh', tokens[2]])
        elif str(tokens[1]) == 'status':
            return channel, check_output(['git', 'status'])

    return channel, '...'
