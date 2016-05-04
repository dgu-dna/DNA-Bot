# coding: utf-8
from __future__ import unicode_literals
import json
import re

TOKENIZE_PATTERN = re.compile(r'["“](.+?)["”]|(\S+)', re.U | re.S)
SETTING_PATH = './unit.json'

settings = json.loads(open(SETTING_PATH).read())

COMMANDS = ['!테스트', '!test', '!ㅌㅅㅌ', '!tst']


def run(robot, channel, tokens, user):
    '''테스트할 프로시져를 여기에 추가하세용!'''
    msg = 'Unknown Command'
    if tokens is not None:
        msg = ''
        for token in tokens:
            msg = msg + token + ' '
    return channel, msg


def extractTokens(message):
    tokens = filter(lambda x: x and x.strip(), TOKENIZE_PATTERN.split(message))
    for command in COMMANDS:
        if tokens[0] == command:
            return tokens[1:]
    return None


def createParams(input_str):
    robot = None
    channel = settings['channel']
    if channel == '':
        channel = settings['CHANNELS']['C0SNZ83TK']
    tokens = extractTokens(settings['tokens'] + input_str)
    user = settings['user']
    return robot, channel, tokens, user

input_str = ''
while input_str != 'exit':
    print 'The input message : ',
    input_str = raw_input()
    robot, channel, message, user = createParams(input_str)
    channel, message = run(robot, channel, message, user)
    print 'To. ' + channel + " From. " + settings['USERS'][user]
    print message
