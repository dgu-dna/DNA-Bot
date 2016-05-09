# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import cat_token


@on_command(['!계산'])
def run(robot, channel, tokens, user, command):
    '''간단한 수식 계산'''
    msg = '사용법 오류'
    returnType = 'DEC'
    formula = ''
    for idx, token in enumerate(tokens):
        token = str(token).lower()
        if token in ['hex', '16진수']:
            returnType = 'HEX'
        elif token in ['oct', '8진수']:
            returnType = 'OCT'
        elif token in ['bin', '2진수']:
            returnType = 'BIN'
        else:
            formula = cat_token(tokens, idx)
            msg = eval(formula)
            break
    if returnType == 'HEX':
        msg = hex(msg)
    elif returnType == 'OCT':
        msg = oct(msg)
    elif returnType == 'BIN':
        msg = bin(msg)
    else:
        msg = str(msg)
    return channel, formula + ' = ' + msg
