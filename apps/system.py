# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
import subprocess
import sys
import os
from subprocess import check_output
import imp
import json
settings = imp.load_source('settings','./settings.py')
BOT_NAME = settings.BOT_NAME
ICON_URL = settings.ICON_URL

def send_msg(robot, channel, txt):
    try:
        robot.client.api_call('chat.postMessage',username=BOT_NAME+' 매니저', as_user='false',icon_url=ICON_URL,channel=channel,text=txt)
    except:
        robot.client.rtm_send_message(channel, message)

@on_command(['$'])
def run(robot, channel, tokens, user, command):
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
    if str(tokens[0]) == 'statistic':
        msg = '현재 승규는...\n';
        mem_json = json.loads(open('./apps/memo_cache/memo_cache.json').read())
        mem_num = 0
        for value in mem_json.values():
            mem_num += len(value)
        msg += str(len(mem_json.keys())) + '명이 기억시킨,\n'
        msg += str(mem_num) + '개의 메모를 기억하고 있으며\n';
        name_num = len(os.listdir('./apps/name_cache'))
        msg += str(name_num) + '개의 단어 뜻을 기억하고 있고\n';
        quiz_dir = './apps/quiz_cache/category/'
        quiz_list = os.listdir(quiz_dir)
        msg += str(len(quiz_list)) + '개의 문제집에 있는,\n';
        quiz_num = 0
        for quiz in quiz_list:
            quiz_json = json.loads(open(quiz_dir+quiz).read())
            quiz_num += quiz_json['q_num']
        msg += str(quiz_num) + '개의 문제를 기억하고 있고\n';
        word_dir = './apps/game_cache/'
        word_json = json.loads(open(word_dir + 'relay.json').read())
        word_num = len(word_json.keys())
        msg += str(word_num) + '개의 단어 자체를 기억하고 있음.'
        send_msg(robot, channel, msg)
        sys.exit()
    sys.exit()
