# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from slackutils import cat_token, insert_dot, get_nickname
from time import localtime, strftime
from datetime import datetime
import os
import json
import time
import random
import re

CACHE_PATH = './apps/quiz_cache/'
CATEGORY_PATH = CACHE_PATH + 'category/'

def splitanswer(ans):
    answer = re.sub(r'\s*\(.*\)','',ans)
    hint = re.sub(r'.*\(','(',ans)
    if hint == ans:
        hint = ''
    return answer, hint

@on_command(['!정답','!ㅈㄷ','!we'])
def run(robot, channel, tokens, user):
    ''''''
    nickname = get_nickname(user)
    quiz = {}
    if len(tokens) < 1 :
        return channel, '자세한 사용법은 ...'

    if os.path.isfile(CACHE_PATH + nickname + '.json'):
        udat = open(CACHE_PATH + nickname + '.json').read()
        user_info = json.loads(udat)
        qdat = open(CATEGORY_PATH + user_info['category']+'.json').read()
        quiz = json.loads(qdat)
        try_answer = ''
        answer = ''
        for word in cat_token(tokens, 0).split(' '):
            try_answer += word
        for word in cat_token(user_info['answer'], 0).split(' '):
            answer += word
        answer, hint = splitanswer(answer)
        msg = '정답은 `' + answer + '` ' + hint + ' (출제:'+insert_dot(quiz['user'][user_info['q_num']-1])+')'
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
            os.remove(CACHE_PATH + nickname + '.json')
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
        with open(CACHE_PATH + nickname +'.json','w') as fp:
            json.dump(user_info, fp, indent = 4)
        msg += '\n> *['+user_info['category']+']---- '+str(rand_num+1)+'번 문제  || 총 '+str(user_info['q_max'])+'문제 중 '+str(len(user_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+question+'```'
    elif os.path.isfile(CACHE_PATH + str(channel) + '.json'):
        cdat = open(CACHE_PATH + str(channel) + '.json').read()
        chan_info = json.loads(cdat)
        qdat = open(CATEGORY_PATH + chan_info['category'] + '.json').read()
        quiz = json.loads(qdat)
        try_answer = ''
        answer, hint = splitanswer(chan_info['answer'])
        # try_answer = re.sub(r'\s', '', cat_token(tokens, 0))
        try_answer = re.sub(r'\s*\*\s*|~|\?|\[|\]|♥|\.|!|_|,|\s', '', cat_token(tokens,0))
        comp_answer = re.sub(r'\s*\*\s*|~|\?|\[|\]|♥|\.|!|_|,|\s', '', answer)
        # for word in cat_token(tokens, 0).split(' '):
        #     try_answer += word
        # for word in cat_token(chan_info['answer'], 0).split(' '):
        #     answer += word
        msg = '정답은 `'+answer+'` '+hint+' (출제:'+insert_dot(quiz['user'][chan_info['q_num']-1])+')'
        if comp_answer.lower() == try_answer.lower():
            chan_info['solved'].append(chan_info['q_num'])
            msg = ':o: '+ insert_dot(nickname) +', 맞았음. '+msg
            chan_info['correct'] += 1
            if nickname in chan_info['correct_user']:
                chan_info['correct_cnt'][chan_info['correct_user'].index(nickname)] += 1
            else:
                chan_info['correct_user'].append(nickname)
                chan_info['correct_cnt'].append(1)
        else:
            msg = ':x: '+insert_dot(nickname)+', 틀렸음'
            return channel, msg
        if len(chan_info['solved']) >= chan_info['q_max']:
            tim = chan_info['start_time'].split(' ')
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
            msg += '\n문제집 내의 모든 문제를 품. '+str(chan_info['correct'])+'/'+str(chan_info['q_max'])+'문제 정답. (소요시간 : '+elap+')\n'
            userlist = chan_info['correct_user']
            countlist = chan_info['correct_cnt']
            countlist, userlist = zip(*reversed(sorted(zip(countlist, userlist))))
            for user in userlist:
                if userlist.index(user) == 0:
                    msg += ':trophy:  '+insert_dot(user) +': '+str(countlist[userlist.index(user)])+'문제\n'
                else:
                    msg += ' '*9+insert_dot(user) +': '+str(countlist[userlist.index(user)])+'문제\n'
            os.remove(CACHE_PATH + str(channel) + '.json')
            return channel, msg
        rand_num = random.randrange(0, quiz['q_num'])
        #print 'get randnum'+str(rand_num)
        while rand_num+1 in chan_info['solved']:
            rand_num = random.randrange(0, quiz['q_num'])
            #print 'reget randnum'+str(rand_num)
        #print 'insert randnum'
        question = quiz['question'][rand_num]
        answer = quiz['answer'][rand_num]
        chan_info['q_num'] = rand_num+1
        chan_info['question'] = question
        chan_info['answer'] = answer
        chan_info['skip_count'] = []
        with open(CACHE_PATH+str(channel)+'.json','w') as fp:
            json.dump(chan_info, fp, indent = 4)
        msg += '\n> `채널 전체 문제`\n> *['+chan_info['category']+']---- '+str(rand_num+1)+'번 문제  || 총 '+str(chan_info['q_max'])+'문제 중 '+str(len(chan_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+question+'```'
    else:
        return channel, '진행중인 문제집이 없음. 자세한 사용법은...(`!도움 퀴즈`)'
    return channel, msg
