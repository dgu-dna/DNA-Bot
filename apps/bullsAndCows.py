# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import get_nickname, isNumber
from apps.gameInfo import GAME_LIST
from apps.game import *
import re
import os
import json
import random
CACHE_DEFAULT_URL = './apps/game_cache/'
GAME_NAME = re.sub(r'.*/([a-zA-Z]*)\.py.?', r'\1', __file__)


def gameInit(channelInfo):
    # Initialize Game
    num_range = 16 if channelInfo['hexMode'] == 1 else 10
    digit = channelInfo['digit']
    rand_list = random.sample(range(1, num_range), digit)
    channelInfo['answer'] = [format(number, 'X') for number in rand_list]


@on_command(['!숫자야구', '!ㅅㅈㅇㄱ'])
def run(robot, channel, tokens, user):
    ''''''
    jsonFile = CACHE_DEFAULT_URL + str(channel) + '.json'
    stat, stat_msg, channelInfo = checkStatus(channel, tokens, GAME_NAME)
    if stat == -1:      # Error
        return channel, stat_msg
    elif stat == 1:     # Need to initialize
        gameInit(channelInfo)

    userName = get_nickname(user)
    if not channelInfo['member'][channelInfo['index']] == userName:
        return channel, getMessage(MESSAGE_TYPE_CURRENT_USER, channel=channel)
    if not len(tokens[0]) == channelInfo['digit']:  # or isNumber(tokens[0])
        return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)
    strike, ball = 0, 0
    for number in tokens[0]:
        if number == channelInfo['answer'][tokens[0].index(number)]:
            strike += 1
        elif number in channelInfo['answer']:
            ball += 1
    if strike == channelInfo['digit']:
        os.remove(CACHE_DEFAULT_URL + str(channel) + '.json')
        return channel, '정답. 게임종료'
    else:
        channelInfo['index'] += 1
        channelInfo['index'] %= len(channelInfo['member'])
        with open(jsonFile, 'w') as fp:
            json.dump(channelInfo, fp, indent=4)
        result = 'S' + str(strike) + ' B' + str(ball)
        next_user = getMessage(MESSAGE_TYPE_CURRENT_USER, channel=channel)
        return channel, result + '\n' + next_user
    return channel, getMessage(MESSAGE_TYPE_ILLEGAL_SYNTAX)
