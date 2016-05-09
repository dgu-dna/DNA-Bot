# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from slackutils import get_nickname, isNumber
from gameInfo import GAME_LIST, GAME_INFO, MODE_LIST
import os
import json
import time
import urllib
import random
CACHE_DEFAULT_URL = './apps/game_cache/'

STATUS_GAME_READY = 1
STATUS_GAME_START = 2

MESSAGE_TYPE_NONE_GAME = 1
MESSAGE_TYPE_GAME_MEMBER = 2
MESSAGE_TYPE_ILLEGAL_SYNTAX = 3
MESSAGE_TYPE_MAKE_GAME = 4
MESSAGE_TYPE_ALREADY_MEMBER = 5
MESSAGE_TYPE_JOIN_MEMBER = 6
MESSAGE_TYPE_PLAYED_GAME = 7
MESSAGE_TYPE_CURRENT_USER = 8
MESSAGE_TYPE_GAME_NOT_EXIST = 9
MESSAGE_TYPE_GAME_READY = 10
MESSAGE_TYPE_ANOTHER_GAME = 11
MESSAGE_TYPE_GAME_START = 12
MESSAGE_TYPE_FEW_MEMBER = 13
MESSAGE_TYPE_EXIT_MEMBER = 14
MESSAGE_TYPE_GAME_END = 15


def getMessage(type, channel=None, gameName=None):
    if type == MESSAGE_TYPE_NONE_GAME:
        return '진행중인 게임 없음. 자세한 사용법은...(`!도움 게임`)'
    elif type == MESSAGE_TYPE_GAME_MEMBER:
        if channel is None:
            print('''
            You need to pass argument "channel" for MESSAGE_TYPE_GAME_MEMBER
            ''')
            return 'Exception ! Please switch on debug mode'
        if os.path.isfile(CACHE_DEFAULT_URL + str(channel) + '.json'):
            loadDta = open(CACHE_DEFAULT_URL + str(channel) + '.json').read()
            channelInfo = json.loads(loadDta)
            msg = '>*' + channelInfo['name'] + '* '
            modeList = MODE_LIST[channelInfo['name'].encode('utf-8')]
            for key in modeList.keys():
                msg += ('`' + key + ': ' +
                        str(channelInfo[modeList[key][0]]) + '` ')
            msg += '\n> [참가 중인 멤버]\n'
            mems = [(str(i+1), v) for i, v in enumerate(channelInfo['member'])]
            jmems = map(''.join, mems)
            msg += '\n'.join(map(lambda (s): '>*'+s[:1]+'.* '+s[1:], jmems))
            if channelInfo['status'] == STATUS_GAME_READY:
                msg += '\n게임 대기 중...'
            elif channelInfo['status'] == STATUS_GAME_START:
                msg += ('\n' +
                        getMessage(MESSAGE_TYPE_CURRENT_USER, channel=channel))
            return msg
        else:
            return getMessage(MESSAGE_TYPE_NONE_GAME)
    elif type == MESSAGE_TYPE_ILLEGAL_SYNTAX:
        return '자세한 사용법은...(`!도움 게임`)'
    elif type == MESSAGE_TYPE_MAKE_GAME:
        return '방 생성 성공'
    elif type == MESSAGE_TYPE_ALREADY_MEMBER:
        return '이미 참가한 유저'
    elif type == MESSAGE_TYPE_JOIN_MEMBER:
        return '참가 성공'
    elif type == MESSAGE_TYPE_PLAYED_GAME:
        return '이미 게임이 시작됨'
    elif type == MESSAGE_TYPE_CURRENT_USER:
        if channel is None:
            print('''
            You need to pass argument "channel" for MESSAGE_TYPE_CURRENT_USER
            ''')
            return 'Exception ! Please switch on debug mode'
        if os.path.isfile(CACHE_DEFAULT_URL + str(channel) + '.json'):
            loadDta = open(CACHE_DEFAULT_URL + str(channel) + '.json').read()
            channelInfo = json.loads(loadDta)
            if channelInfo['status'] == STATUS_GAME_READY:
                return getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)
            elif channelInfo['status'] == STATUS_GAME_START:
                msg = (':exclamation: 현재 ' +
                       channelInfo['member'][channelInfo['index']] +
                       '님의 차례 :exclamation:')
            return msg
    elif type == MESSAGE_TYPE_GAME_NOT_EXIST:
        return '존재하지 않는 게임임'
    elif type == MESSAGE_TYPE_GAME_READY:
        return '아직 게임이 준비중임...'
    elif type == MESSAGE_TYPE_ANOTHER_GAME:
        return '다른 게임이 진행중임...'
    elif type == MESSAGE_TYPE_FEW_MEMBER:
        if gameName is None:
            print('''
            You need to pass argument "gameName" for MESSAGE_TYPE_CURRENT_USER
            ''')
            return 'Exception ! Please switch on debug mode'
        minMember = GAME_INFO[gameName]['MIN_NEED_PERSON']
        msg = ('인원이 모자랍니다. ' + gameName + '을(를) 플레이하기 위해서는 ' +
               '최소 ' + str(minMember) + '명이 필요합니다.')
        return msg
    elif type == MESSAGE_TYPE_EXIT_MEMBER:
        return '게임에서 나가셨습니다.'
    elif type == MESSAGE_TYPE_GAME_END:
        return '게임이 종료되었습니다'


@on_command(['!게임'])
def run(robot, channel, tokens, user):
    '''게임 함'''

    jsonFile = CACHE_DEFAULT_URL + str(channel) + '.json'
    userName = get_nickname(user)
    channelInfo = {}

    if len(tokens) < 1:
        return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)

    if str(tokens[0]) in ['방생성', '생성']:     # To do: Deny DM
        if len(tokens) < 2:
            return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)
        gameName = ''
        if str(tokens[1]) in GAME_LIST:
            gameName = str(tokens[1])
            if str(tokens[1]) in MODE_LIST:
                modeList = MODE_LIST[str(tokens[1])]
                for mode in modeList.values():
                    channelInfo[mode[0]] = mode[2]
                if len(tokens) > 2:
                    mode = ''
                    for token in tokens[2:]:
                        if isNumber(token):
                            if mode:
                                channelInfo[modeList[mode][0]] = int(token)
                                mode = ''
                        else:
                            mode = str(token)
                            channelInfo[modeList[mode][0]] = 1
        else:
            return channel, getMessage(MESSAGE_TYPE_GAME_NOT_EXIST)
        if not os.path.isfile(jsonFile):
            channelInfo['init'] = True
            channelInfo['index'] = 0
            channelInfo['mode'] = 0
            channelInfo['name'] = gameName
            channelInfo['status'] = STATUS_GAME_READY
            channelInfo['member'] = [userName]
            channelInfo['number'] = []
            channelInfo['reserveExit'] = []
        else:
            return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)

        with open(jsonFile, 'w') as fp:
            json.dump(channelInfo, fp, indent=4)
        return channel, getMessage(MESSAGE_TYPE_MAKE_GAME)
    else:
        if not os.path.isfile(jsonFile):
            return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)

    loadDta = open(jsonFile).read()
    channelInfo = json.loads(loadDta)

    if str(tokens[0]) in ['참가', '방참가', '참여']:
        if userName in channelInfo['member']:
            return channel, userName + getMessage(MESSAGE_TYPE_ALREADY_MEMBER)
        if channelInfo['status'] == STATUS_GAME_START:
            return channel, userName + getMessage(MESSAGE_TYPE_PLAYED_GAME)
        channelInfo['member'].append(userName)
        with open(jsonFile, 'w') as fp:
            json.dump(channelInfo, fp, indent=4)
        return channel, str(userName) + getMessage(MESSAGE_TYPE_JOIN_MEMBER)

    if str(tokens[0]) == '시작':
        if channelInfo['status'] == STATUS_GAME_START:
            return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)
        gName = channelInfo['name'].encode('utf-8')
        gInfo = GAME_INFO[gName]
        if len(channelInfo['member']) < gInfo['MIN_NEED_PERSON']:
            return channel, getMessage(MESSAGE_TYPE_FEW_MEMBER, gameName=gName)
        channelInfo['status'] = STATUS_GAME_START
        with open(jsonFile, 'w') as fp:
            json.dump(channelInfo, fp, indent=4)
        return channel, getMessage(MESSAGE_TYPE_GAME_MEMBER, channel=channel)

    if str(tokens[0]) == '상태':
        return channel, getMessage(MESSAGE_TYPE_GAME_MEMBER, channel=channel)

    if str(tokens[0]) == '나가기':
        gName = channelInfo['name'].encode('utf-8')
        gInfo = GAME_INFO[gName]
        if gInfo['ALLOW_EXIT'] == 1:
            if userName in channelInfo['member']:
                channelInfo['member'].remove(userName)
                channelInfo['index'] %= len(channelInfo['member'])
                with open(jsonFile, 'w') as fp:
                    json.dump(channelInfo, fp, indent=4)
                return channel, getMessage(MESSAGE_TYPE_EXIT_MEMBER)
            else:
                return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)
        else:
            # 전원 투표시 게임 종료 구현예정
            return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)
        if len(channelInfo['member']) == 0:
            os.remove(jsonFile)
            return channel, getMessage(MESSAGE_TYPE_GAME_END)

    # if str(tokens[0]) == '조회':
    return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////
#    elif str(tokens[0]) == '포기':
#        os.remove('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json')
#        msg = '진행중인 퀴즈를 포기함'
#        return channel, msg
#    elif str(tokens[0]) == '다같이포기':
#        cdat = open('./apps/quiz_cache/'+str(channel)+'.json').read()
#        chan_info = json.loads(cdat)
#        if str(user) in chan_info['give_up']:
#            return channel, '이미 포기에 투표함'
#        if len(chan_info['give_up']) < 2:
#            chan_info['give_up'].append(str(user))
#            with open('./apps/quiz_cache/'+str(channel)+'.json','w') as fp:
#            return channel, str(3-len(chan_info['give_up']))+'명 더 필요함'
#        os.remove('./apps/quiz_cache/'+str(channel)+'.json')
#        msg = '진행중인 *채널 전체 퀴즈* 를 포기함'
#        return channel, msg
#    elif str(tokens[0]) == '조회':
#        if len(tokens) < 2 :
#            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
#        qdat = open('./apps/quiz_cache/category/'+str(tokens[1])+'.json').read()
#        quiz = json.loads(qdat)
#        msg = str(tokens[1])+'에는 총 '+str(quiz['q_num'])+'개의 문제가 있음'
#        return channel, msg
#    elif str(tokens[0]) == '문제집':
#        all_file = check_output(['ls', './apps/quiz_cache/category'])
#        msg = '>*여태 등록된 문제집들*\n'
#        for s in all_file.split('\n'):
#            msg += s[:-5]+' || '
#        msg = msg[:-8]
#        return channel, msg
#    elif str(tokens[0]) == '시작':
#        if len(tokens) < 2 :
#            return channel, '자세한 사용법은...(`!도움 퀴즈`)'
#        if os.path.isfile('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json'):
#            return channel, '이미 진행중인 문제집이 있음. `!퀴즈`'
#        if not os.path.isfile('./apps/quiz_cache/category/'+str(tokens[1])+'.json'):
#            return channel, '그런 문제집은 없음.'
#        qdat = open('./apps/quiz_cache/category/'+str(tokens[1])+'.json').read()
#        quiz = json.loads(qdat)
#        rand_num = random.randrange(0, quiz['q_num'])
#        question = quiz['question'][rand_num]
#        answer = quiz['answer'][rand_num]
#        user_info = {}
#        user_info['name'] = str(user_data['user']['name'])
#        user_info['start_time'] = strftime('%Y %m %d %H %M %S', localtime())
#        user_info['solved'] = []
#        user_info['correct'] = 0
#        user_info['q_num'] = rand_num+1
#        user_info['q_max'] = quiz['q_num']
#        user_info['question'] = question
#        user_info['answer'] = answer
#        user_info['category'] = str(tokens[1])
#        with open('./apps/quiz_cache/'+str(user_data['user']['name'])+'.json','w') as fp:
#            json.dump(user_info, fp, indent = 4)
#        msg = '> *['+str(tokens[1])+']---- '+str(rand_num+1)+'번 문제  || 총 '+str(user_info['q_max'])+'문제 중 '+str(len(user_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+question+'```'
#    elif str(tokens[0]) == '다같이시작':
#        if os.path.isfile('./apps/quiz_cache/'+str(channel)+'.json'):
#            return channel, '이미 진행중인 문제집이 있음. `!퀴즈`'
#        if not os.path.isfile('./apps/quiz_cache/category/'+str(tokens[1])+'.json'):
#            return channel, '그런 문제집은 없음.'
#        qdat = open('./apps/quiz_cache/category/'+str(tokens[1])+'.json').read()
#        quiz = json.loads(qdat)
#        rand_num = random.randrange(0, quiz['q_num'])
#        question = quiz['question'][rand_num]
#        answer = quiz['answer'][rand_num]
#        chan_info = {}
#        chan_info['start_time'] = strftime('%Y %m %d %H %M %S', localtime())
#        chan_info['last_solved'] = int(round(time.time()*1000))
#        chan_info['solved'] = []
#        chan_info['correct'] = 0
#        chan_info['give_up'] = []
#        chan_info['skip_count'] = []
#        chan_info['correct_user'] = []
#        chan_info['correct_cnt'] = []
#        chan_info['q_num'] = rand_num+1
#        if len(tokens) == 3:
#            chan_info['q_max'] = int(tokens[2])
#        else:
#            chan_info['q_max'] = quiz['q_num']
#        chan_info['question'] = question
#        chan_info['answer'] = answer
#        chan_info['category'] = str(tokens[1])
#        with open('./apps/quiz_cache/'+str(channel)+'.json','w') as fp:
#            json.dump(chan_info, fp, indent = 4)
#        msg = '> `채널 전체 문제`\n> *['+str(tokens[1])+']---- '+str(rand_num+1)+'번 문제  || 총 '+str(chan_info['q_max'])+'문제 중 '+str(len(chan_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+question+'```'
#    elif str(tokens[0]) == '패스':
#        if not os.path.isfile('./apps/quiz_cache/'+str(channel)+'.json'):
#            return channel, '자세한 사용법은... `!퀴즈`'
#        cdat = open('./apps/quiz_cache/'+str(channel)+'.json').read()
#        chan_info = json.loads(cdat)
#        if str(user) in chan_info['skip_count']:
#            return channel, '이미 패스에 투표함'
#        if len(chan_info['skip_count']) < 1:
#            chan_info['skip_count'].append(str(user))
#            with open('./apps/quiz_cache/'+str(channel)+'.json','w') as fp:
#                json.dump(chan_info, fp, indent = 4)
#            return channel, str(2-len(chan_info['skip_count']))+'명 더 필요함'
#        qdat = open('./apps/quiz_cache/category/'+chan_info['category']+'.json').read()
#        quiz = json.loads(qdat)
#        answer, hint = splitanswer(chan_info['answer'])
#        msg = '정답은 `'+answer+'` '+hint+' (출제:'+quiz['user'][chan_info['q_num']-1][:1]+'·'+quiz['user'][chan_info['q_num']-1][1:]+')\n'
#        chan_info['solved'].append(chan_info['q_num'])
#        rand_num = random.randrange(0, quiz['q_num'])
#        while rand_num+1 in chan_info['solved']:
#            rand_num = random.randrange(0, quiz['q_num'])
#        question = quiz['question'][rand_num]
#        answer = quiz['answer'][rand_num]
#        chan_info['last_solved'] = int(round(time.time()*1000))
#        chan_info['q_num'] = rand_num+1
#        chan_info['question'] = question
#        chan_info['answer'] = answer
#        chan_info['skip_count'] = []
#        with open('./apps/quiz_cache/'+str(channel)+'.json','w') as fp:
#            json.dump(chan_info, fp, indent = 4)
#        msg = msg+'> `채널 전체 문제`\n> *['+chan_info['category']+']---- '+str(rand_num+1)+'번 문제  || 총 '+str(chan_info['q_max'])+'문제 중 '+str(len(chan_info['solved'])+1)+'개 째... || 답안 제출법:* `!정답 <답안>`\n```'+question+'```'
#    else:
#        msg = '자세한 사용법은...(`!도움 퀴즈`)'
#    return channel, msg


def checkStatus(channel, tokens, name):
    if len(tokens) < 1:
        return -1, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX), None
    jsonFile = CACHE_DEFAULT_URL + str(channel) + '.json'
    if not os.path.isfile(jsonFile):
        return -1, getMessage(MESSAGE_TYPE_NONE_GAME), None
    loadDta = open(jsonFile).read()
    channelInfo = json.loads(loadDta)
    if channelInfo['status'] == STATUS_GAME_READY:
        return -1, getMessage(MESSAGE_TYPE_GAME_READY), None
    if GAME_LIST[channelInfo['name'].encode('utf-8')] != name:
        return -1, getMessage(MESSAGE_TYPE_ANOTHER_GAME), None
    if channelInfo['init'] is True:
        channelInfo['init'] = False
        return 1, '', channelInfo
    return 0, '', channelInfo
