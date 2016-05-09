# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import cat_token, isNumber, get_nickname
from time import localtime, strftime
from subprocess import check_output
import os
import re
import json
import time
import urllib
import random
import imp
settings = imp.load_source('settings', './settings.py')
WEB_API_TOKEN = settings.WEB_API_TOKEN
CACHE_DEFAULT_URL = './apps/quiz_cache/'
CACHE_CATEGORY_URL = './apps/quiz_cache/category/'


def get_random_question(channel):
    infoFile = CACHE_DEFAULT_URL + channel + '.json'
    cdat = json.loads(open(infoFile).read())
    quizRaw = open(CACHE_CATEGORY_URL + cdat['category'] + '.json').read()
    qdat = json.loads(quizRaw)
    cdat['solved'].append(cdat['q_num'])
    rand_num = random.randrange(0, qdat['q_num'])
    while rand_num + 1 in cdat['solved']:
        rand_num = random.randrange(0, qdat['q_num'])
    question = qdat['question'][rand_num]
    answer = qdat['answer'][rand_num]
    cdat['last_solved'] = int(round(time.time() * 1000))
    cdat['q_num'] = rand_num + 1
    cdat['question'] = question
    cdat['answer'] = answer
    cdat['skip_count'] = []
    cdat['give_up'] = []
    with open(infoFile, 'w') as fp:
        json.dump(cdat, fp, indent=4)


def get_answer(channel):
    cdat = json.loads(open(CACHE_DEFAULT_URL + channel + '.json').read())
    answer = re.sub(r'\s*\(.*\)', '', cdat['answer'])
    hint = re.sub(r'.*\(', '(', cdat['answer'])
    if hint == cdat['answer']:
        hint = ''
    return answer, hint


def get_message(channel):
    msg = ''
    if channel[0] == 'C':
        msg += '> `채널 전체 문제`\n'
    if os.path.isfile(CACHE_DEFAULT_URL + channel + '.json'):
        channelRaw = open(CACHE_DEFAULT_URL + channel + '.json').read()
        cdat = json.loads(channelRaw)
    else:
        return '진행 중인 퀴즈가 없음. `!도움 퀴즈`'
    msg += ('> *['+cdat['category']+']---- ' +
            unicode(cdat['q_num']) + '번 문제  || 총 ' +
            unicode(cdat['q_max']) + '문제 중 ' +
            unicode(len(cdat['solved']) + 1) +
            '개 째... || 답안 제출법:* `!정답 <답안>`\n```' +
            cdat['question'] + '```')
    return msg


@on_command(['!퀴즈'])
def run(robot, channel, tokens, user):
    '''문제 내드림'''
    infoFile = CACHE_DEFAULT_URL + channel + '.json'
    nickname = get_nickname(user)
    msg = ''
    if len(tokens) < 1:
        return channel, get_message(channel)

    if tokens[0] in ['등록', '추가']:
        if len(tokens) != 4:
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        quizFile = CACHE_CATEGORY_URL + tokens[1] + '.json'
        qdat = {}
        if os.path.isfile(quizFile):
            qdat = json.loads(open(quizFile).read())
            qdat['q_num'] += 1
            qdat['question'].append(tokens[2])
            qdat['answer'].append(tokens[3])
            qdat['user'].append(nickname)
            qdat['time'].append(strftime('%Y-%m-%d %H:%M:%S', localtime()))
        else:
            qdat['q_num'] = 1
            qdat['question'] = [tokens[2]]
            qdat['answer'] = [tokens[3]]
            qdat['user'] = [nickname]
            qdat['time'] = [strftime('%Y-%m-%d %H:%M:%S', localtime())]
        with open(quizFile, 'w') as fp:
            json.dump(qdat, fp, indent=4)
        msg = tokens[1] + '에 관한 문제가 추가됨'

    elif tokens[0] == '수정':
        if len(tokens) != 5:
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        quizFile = CACHE_CATEGORY_URL + tokens[1] + '.json'
        qdat = json.loads(open(quizFile).read())
        if not isNumber(tokens[2]):
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        idx = int(tokens[2]) - 1
        quiz['question'][idx] = tokens[3]
        quiz['answer'][idx] = tokens[4]
        quiz['user'][idx] = nickname
        quiz['time'][idx] = strftime('%Y-%m-%d %H:%M:%S', localtime())
        with open(quizFile, 'w') as fp:
            json.dump(qdat, fp, indent=4)
        msg = tokens[1] + '에 관한 ' + tokens[2] + '번 문제가 수정됨'

    elif tokens[0] == '포기':
        if channel[0] == 'D':
            os.remove(infoFile)
            return channel, '진행중인 퀴즈를 포기함'
        cdat = json.loads(open(infoFile).read())
        if user in cdat['give_up']:
            return channel, '이미 포기에 투표함'
        if len(cdat['give_up']) < 2:
            cdat['give_up'].append(user)
            with open(infoFile, 'w') as fp:
                json.dump(cdat, fp, indent=4)
            return channel, unicode(3 - len(cdat['give_up']))+'명 더 필요함'
        os.remove(cdat)
        msg = '진행중인 퀴즈 를 포기함'

    elif tokens[0] == '조회':
        if len(tokens) < 2:
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        if channel[0] == 'C':
            return channel, '채널에선 사용할 수 없음'
        quizFile = CACHE_CATEGORY_URL + tokens[1] + '.json'
        qdat = json.loads(open(quizFile).read())
        msg = tokens[1] + '에는 총 ' + unicode(qdat['q_num']) + '개의 문제가 있음'
        for idx, question in enumerate(qdat['question']):
            msg += '\n*' + unicode(idx + 1) + '.* ' + question

    elif tokens[0] == '문제집':
        all_file = check_output(['ls', CACHE_CATEGORY_URL])
        all_file = re.sub('.json', '', all_file)
        # all_file = re.sub('.\n', ' || ', all_file)
        msg = '>*여태 등록된 문제집들*\n' + ' || '.join(all_file.split('\n'))
        # msg += ' || '.join(all_file.split('.json\n'))
        # for s in all_file.split('\n'):
        #     msg += s[:-5]+' || '
        # msg = msg[:-8]

    elif tokens[0] == '시작':
        if len(tokens) < 2:
            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
        if os.path.isfile(infoFile):
            return channel, '이미 진행중인 문제집이 있음. `!퀴즈`'
        if not os.path.isfile(CACHE_CATEGORY_URL + tokens[1] + '.json'):
            return channel, '그런 문제집은 없음.'
        quizRaw = open(CACHE_CATEGORY_URL + tokens[1] + '.json').read()
        qdat = json.loads(quizRaw)
        rand_num = random.randrange(0, qdat['q_num'])
        question = qdat['question'][rand_num]
        answer = qdat['answer'][rand_num]
        cdat = {}
        cdat['name'] = nickname
        cdat['start_time'] = strftime('%Y %m %d %H %M %S', localtime())
        cdat['last_solved'] = int(round(time.time() * 1000))
        cdat['solved'] = []
        cdat['correct'] = 0
        cdat['give_up'] = []
        cdat['skip_count'] = []
        cdat['correct_user'] = []
        cdat['correct_cnt'] = []
        cdat['q_num'] = rand_num + 1
        if len(tokens) == 3:
            cdat['q_max'] = int(tokens[2])
        else:
            cdat['q_max'] = qdat['q_num']
        cdat['question'] = question
        cdat['answer'] = answer
        cdat['category'] = tokens[1]
        with open(infoFile, 'w') as fp:
            json.dump(cdat, fp, indent=4)
        msg = get_message(channel)

    elif tokens[0] == '패스':
        if not os.path.isfile(infoFile):
            return channel, '자세한 사용법은... `!퀴즈`'
        cdat = json.loads(open(infoFile).read())
        if user in cdat['skip_count']:
            return channel, '이미 패스에 투표함'
        if len(cdat['skip_count']) < 1:
            cdat['skip_count'].append(user)
            with open(infoFile, 'w') as fp:
                json.dump(cdat, fp, indent=4)
            return channel, unicode(2 - len(cdat['skip_count'])) + '명 더 필요함'
        quizRaw = open(CACHE_CATEGORY_URL + cdat['category'] + '.json').read()
        qdat = json.loads(quizRaw)
        answer, hint = get_answer(channel)
        msg = '정답은 `'+answer+'` '+hint+' (출제:'+quiz['user'][chan_info['q_num']-1][:1]+'·'+quiz['user'][chan_info['q_num']-1][1:]+')\n'
        get_random_question(channel)
        msg += get_message(channel)
    else:
        msg = '자세한 사용법은...(`!도움 퀴즈`)'
    return channel, msg
