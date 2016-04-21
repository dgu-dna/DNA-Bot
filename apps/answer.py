# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from slackudf import cat_token
from time import localtime, strftime
from datetime import datetime
import os
import json
import time
import urllib
import random
import imp
settings = imp.load_source('settings','./settings.py')
WEP_API_TOKEN = settings.WEP_API_TOKEN
#from settings import WEP_API_TOKEN

@on_command(['!정답','!ㅈㄷ','!we'])
def run(robot, channel, tokens, user):
    ''''''
    # channel 'C', DM 'D'
    url = 'https://slack.com/api/users.info?token='+WEP_API_TOKEN+'&user='+str(user)+'&pretty=1'
    response = urllib.urlopen(url)
    user_data = json.loads(response.read())
    quiz = {}
    if len(tokens) < 1 :
        return channel, '자세한 사용법은 ...'

    if os.path.isfile('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json'):
        udat = open('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json').read()
        user_info = json.loads(udat)
        qdat = open('./apps/quiz_cache/category/'+user_info['category']+'.json').read()
        quiz = json.loads(qdat)
        try_answer = ''
        answer = ''
        for word in cat_token(tokens, 0).split(' '):
            try_answer += word
        for word in cat_token(user_info['answer'], 0).split(' '):
            answer += word
        msg = '정답은 `'+user_info['answer']+'` (출제:'+quiz['user'][user_info['q_num']-1][:1]+'·'+quiz['user'][user_info['q_num']-1][1:]+')'
        user_info['solved'].append(user_info['q_num'])
        if answer.lower() == try_answer.lower():
            msg = ':o: '+msg
            user_info['correct'] += 1
        else:
            msg = ':x: '+msg
        if len(user_info['solved']) >= user_info['q_max']:
            tim = user_info['start_time'].split(' ')
            dt_i = datetime(int(tim[0]), int(tim[1]), int(tim[2]), int(tim[3]), int(tim[4]), int(tim[5]), 0)
            dt_f = datetime.today()
            dt = dt_f - dt_i
            sec = dt.total_seconds()
            elap = ''
            if sec // 86400 != 0 :
                elap += str(int(sec // 86400))+'일, '+str(int((sec % 86400) // 3600))+'시간 '+str(int((sec % 3600) // 60))+'분 '+str(int(sec % 60))+'초'
            elif sec // 3600 != 0:
                elap += str(int((sec % 86400) // 3600))+'시간 '+str(int((sec % 3600) // 60))+'분 '+str(int(sec % 60))+'초'
            elif sec // 60 != 0:
                elap += str(int((sec % 3600) // 60))+'분 '+str(int(sec % 60))+'초'
            else:
                elap += str(int(sec % 60))+'초'
            msg += '\n문제집 내의 모든 문제를 품. '+str(user_info['correct'])+'/'+str(user_info['q_max'])+'문제 정답. (소요시간 : '+elap+')'
            os.remove('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json')
            return channel, msg
        rand_num = random.randrange(0, quiz['q_num'])
        #print 'get randnum'+str(rand_num)
        while rand_num+1 in user_info['solved']:
            rand_num = random.randrange(0, quiz['q_num'])
            #print 'reget randnum'+str(rand_num)
        #print 'insert randnum'
        question = quiz['question'][rand_num]
        answer = quiz['answer'][rand_num]
        user_info['q_num'] = rand_num+1
        user_info['question'] = question
        user_info['answer'] = answer
        with open('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json','w') as fp:
            json.dump(user_info, fp, indent = 4)
        msg += '\n> *['+user_info['category']+']---- '+str(rand_num+1)+'번 문제  || 총 '+str(user_info['q_max'])+'문제 중 '+str(len(user_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+question+'```'
    else:
        return channel, '진행중인 문제집이 없음. 자세한 사용법은...(`!도움 퀴즈`)'
    return channel, msg
