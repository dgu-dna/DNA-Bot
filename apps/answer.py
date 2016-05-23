from apps.decorators import on_command
from apps.slackutils import cat_token, insert_dot, get_nickname, get_userinfo, send_msg
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
def run(robot, channel, tokens, user, command):
    ''''''
    info_file = CACHE_PATH + channel + '.json'
    nickname = get_nickname(user)
    qdat = {}
    if len(tokens) < 1:
        return channel, '자세한 사용법은 ... `!도움 퀴즈`'

    if os.path.isfile(info_file):
        cdat = json.loads(open(info_file).read())
        quizRaw = open(CATEGORY_PATH + cdat['category'] + '.json').read()
        qdat = json.loads(quizRaw)
        answer, hint = get_answer(channel)
        msg = json.loads(open(CACHE_PATH + 'attach.json').read())
        try_answer = re.sub(r'\s*\*\s*|~|\?|\[|\]|♥|\.|!|_|,|\s', '', cat_token(tokens,0))
        comp_answer = re.sub(r'\s*\*\s*|~|\?|\[|\]|♥|\.|!|_|,|\s', '', answer)
        msg[0]['author_link'] += nickname
        msg[0]['author_name'] = nickname
        msg[0]['author_icon'] = get_userinfo(user, ['profile', 'image_32'])
        msg[0]['title'] = answer
        msg[0]['text'] = hint
		#msg[0]['field'] = ...
        #msg = '정답은 `'+answer+'` '+hint+' (출제:'+insert_dot(qdat['user'][cdat['q_num']-1])+')\n'

        if comp_answer.lower() == try_answer.lower():
            #msg = ':o: ' + insert_dot(nickname) + ', 맞았음. \n'+msg
            msg[0]['color'] = '#0fb5a1'
            msg[0]['thumb_url'] = 'http://feonfun.com/o_mark.png'
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
                msg = ':x: '+insert_dot(nickname)+', 틀렸음. \n'+msg
        with open(info_file, 'w') as fp:
            json.dump(cdat, fp, indent=4)
        if not get_random_question(channel):    # failed to get question(fin.)
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
            msg[0]['text'] += '\n문제집 내의 모든 문제를 품. '+str(cdat['correct'])+'/'+str(cdat['q_max'])+'문제 정답. (소요시간 : '+elap+')\n'
            userlist = cdat['correct_user']
            countlist = cdat['correct_cnt']
            if len(userlist) > 0:
                countlist, userlist = zip(*sorted(zip(countlist, userlist), reverse=True))
                for user in userlist:
                    if userlist.index(user) == 0:
                        msg[0]['text'] += ':trophy:  '+insert_dot(user) +': '+str(countlist[userlist.index(user)])+'문제\n'
                    else:
                        msg[0]['text'] += ' '*9+insert_dot(user) +': '+str(countlist[userlist.index(user)])+'문제\n'
            os.remove(info_file)
            return channel, msg
        else:
            send_msg(robot, channel, attachments=msg)
            time.sleep(1)
            msg = get_message(channel)
    else:
        return channel, '진행중인 문제집이 없음. 자세한 사용법은...(`!도움 퀴즈`)'
    return channel, msg
