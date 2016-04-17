# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from slackudf import cat_token
from time import localtime, strftime
from subprocess import check_output
import os
import json
import time
import urllib
import random
import imp
settings = imp.load_source('settings','./settings.py')
WEP_API_TOKEN = settings.WEP_API_TOKEN
#from settings import WEP_API_TOKEN

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@on_command(['!퀴즈','!ㅋㅈ','!zw'])
def run(robot, channel, tokens, user):
    '''문제 내드림'''
    # channel 'C', DM 'D'
    url = 'https://slack.com/api/users.info?token='+WEP_API_TOKEN+'&user='+str(user)+'&pretty=1'
    response = urllib.urlopen(url)
    user_data = json.loads(response.read())
    quiz = {}
    if len(tokens) < 1:
        if os.path.isfile('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json'):
            udat = open('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json').read()
            user_info = json.loads(udat)
            msg = '> *['+user_info['category']+']---- '+str(user_info['q_num'])+'번 문제  || 총 '+str(user_info['q_max'])+'문제 중 '+str(len(user_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+user_info['question']+'```'
            return channel, msg
        else:
            return channel, '진행중인 문제집이 없음. 자세한 사용법은...(`!도움 퀴즈`)'

    if str(tokens[0]) == '등록':
        if len(tokens) != 4:
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        if not os.path.isfile('./apps/quiz_cache/category/'+str(tokens[1])+'.json'):
            quiz['q_num'] = 1
            quiz['question'] = [str(tokens[2])]
            quiz['answer'] = [str(tokens[3])]
            quiz['user'] = [str(user_data['user']['name'])]
            quiz['time'] = [strftime('%Y-%m-%d %H:%M:%S', localtime())]
        else:
            qdat = open('./apps/quiz_cache/category/'+str(tokens[1])+'.json').read()
            quiz = json.loads(qdat)
            q_num = quiz['q_num']
            q_num += 1
            quiz['q_num'] = q_num
            quiz['question'].append(str(tokens[2]))
            quiz['answer'].append(str(tokens[3]))
            quiz['user'].append(str(user_data['user']['name']))
            quiz['time'].append(strftime('%Y-%m-%d %H:%M:%S', localtime()))
        with open('./apps/quiz_cache/category/'+str(tokens[1])+'.json','w') as fp:
            json.dump(quiz, fp, indent = 4)
        return channel, str(tokens[1])+'에 관한 문제가 추가됨'
    elif str(tokens[0]) == '수정':
        if len(tokens) < 5 :
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        qdat = open('./apps/quiz_cache/category/'+str(tokens[1])+'.json').read()
        quiz = json.loads(qdat)
        if not isNum(tokens[2]):
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        quiz['question'][int(tokens[2])-1] = tokens[3]
        quiz['answer'][int(tokens[2])-1] = tokens[4]
        quiz['user'][int(tokens[2])-1] = str(user_data['user']['name'])
        quiz['time'][int(tokens[2])-1] = strftime('%Y-%m-%d %H:%M:%S', localtime())
        with open('./apps/quiz_cache/category/'+str(tokens[1])+'.json','w') as fp:
            json.dump(quiz, fp, indent = 4)
        return channel, str(tokens[1])+'에 관한 '+str(tokens[2])+'번 문제가 수정됨'
    elif str(tokens[0]) == '포기':
        os.remove('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json')
        msg = '진행중인 퀴즈를 포기함'
        return channel, msg
    elif str(tokens[0]) == '조회':
        if len(tokens) < 2 :
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        qdat = open('./apps/quiz_cache/category/'+str(tokens[1])+'.json').read()
        quiz = json.loads(qdat)
        msg = str(tokens[1])+'에는 총 '+str(quiz['q_num'])+'개의 문제가 있음'
        return channel, msg
    elif str(tokens[0]) == '문제집':
        all_file = check_output(['ls', './apps/quiz_cache/category'])
        msg = '>*여태 등록된 문제집들*\n'
        for s in all_file.split('\n'):
            msg += s[:-5]+' || '
        msg = msg[:-8]
        return channel, msg
    elif str(tokens[0]) == '시작':
        if len(tokens) < 2 :
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        if os.path.isfile('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json'):
            return channel, '이미 진행중인 문제집이 있음. `!퀴즈`'
        if not os.path.isfile('./apps/quiz_cache/category/'+str(tokens[1])+'.json'):
            return channel, '그런 문제집은 없음.'
        qdat = open('./apps/quiz_cache/category/'+str(tokens[1])+'.json').read()
        quiz = json.loads(qdat)
        rand_num = random.randrange(0, quiz['q_num'])
        question = quiz['question'][rand_num]
        answer = quiz['answer'][rand_num]
        user_info = {}
        user_info['name'] = str(user_data['user']['name'])
        user_info['start_time'] = strftime('%Y %m %d %H %M %S', localtime())
        user_info['solved'] = []
        user_info['correct'] = 0
        user_info['q_num'] = rand_num+1
        user_info['q_max'] = quiz['q_num']
        user_info['question'] = question
        user_info['answer'] = answer
        user_info['category'] = str(tokens[1])
        with open('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json','w') as fp:
            json.dump(user_info, fp, indent = 4)
        msg = '> *['+str(tokens[1])+']---- '+str(rand_num+1)+'번 문제  || 총 '+str(user_info['q_max'])+'문제 중 '+str(len(user_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+question+'```'
    return channel, msg
