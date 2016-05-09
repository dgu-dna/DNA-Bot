from apps.decorators import on_command
from apps.slackutils import cat_token, insert_dot, get_nickname
from time import localtime, strftime
from datetime import datetime
from apps.quiz import get_answer, get_random_question, get_message
import os
import json
import time
import random
import re

CACHE_PATH = './apps/quiz_cache/'
CATEGORY_PATH = CACHE_PATH + 'category/'


def compAnswer(ans1, ans2):

    return True


@on_command(['!정답', '!ㅈㄷ', '!we'])
def run(robot, channel, tokens, user):
    ''''''
    infoFile = CACHE_PATH + channel + '.json'
    nickname = get_nickname(user)
    qdat = {}
    if len(tokens) < 1:
        return channel, '자세한 사용법은 ... `!도움 퀴즈`'

    if os.path.isfile(infoFile):
        cdat = json.loads(open(infoFile).read())
        quizRaw = open(CATEGORY_PATH + cdat['category'] + '.json').read()
        qdat = json.loads(quizRaw)
        answer, hint = get_answer(channel)

        try_answer = re.sub(r'\s*\*\s*|~|\?|\[|\]|♥|\.|!|_|,|\s', '', cat_token(tokens,0))
        comp_answer = re.sub(r'\s*\*\s*|~|\?|\[|\]|♥|\.|!|_|,|\s', '', answer)

        msg = '정답은 `'+answer+'` '+hint+' (출제:'+insert_dot(qdat['user'][cdat['q_num']-1])+')\n'

        if comp_answer.lower() == try_answer.lower():
            cdat['solved'].append(cdat['q_num'])
            msg = ':o: '+ insert_dot(nickname) +', 맞았음. \n'+msg
            cdat['correct'] += 1
            if nickname in cdat['correct_user']:
                cdat['correct_cnt'][cdat['correct_user'].index(nickname)] += 1
            else:
                cdat['correct_user'].append(nickname)
                cdat['correct_cnt'].append(1)
        else:
            if channel[0] == 'C':
                msg = ':x: '+insert_dot(nickname)+', 틀렸음.'
                return channel, msg
            else:
                cdat['solved'].append(cdat['q_num'])
                msg = ':x: '+insert_dot(nickname)+', 틀렸음. \n'+msg

        if len(cdat['solved']) >= cdat['q_max']:
            tim = cdat['start_time'].split(' ')
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
            msg += '\n문제집 내의 모든 문제를 품. '+str(cdat['correct'])+'/'+str(cdat['q_max'])+'문제 정답. (소요시간 : '+elap+')\n'
            userlist = cdat['correct_user']
            countlist = cdat['correct_cnt']
            if len(userlist) > 0:
                countlist, userlist = zip(*sorted(zip(countlist, userlist), reverse=True))
                for user in userlist:
                    if userlist.index(user) == 0:
                        msg += ':trophy:  '+insert_dot(user) +': '+str(countlist[userlist.index(user)])+'문제\n'
                    else:
                        msg += ' '*9+insert_dot(user) +': '+str(countlist[userlist.index(user)])+'문제\n'
            os.remove(infoFile)
            return channel, msg
        get_random_question(channel)
        msg += get_message(channel)
    else:
        return channel, '진행중인 문제집이 없음. 자세한 사용법은...(`!도움 퀴즈`)'
    return channel, msg
