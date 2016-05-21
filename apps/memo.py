# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import cat_token
from time import localtime, strftime
import os
import json
CACHE_DEFAULT_URL = './apps/memo_cache/memo_cache.json'


@on_command(['!메모', '!ㅁㅁ', '!aa'])
def run(robot, channel, tokens, user, command):
    '''메모 기억해드림'''
    jdat = json.loads(open(CACHE_DEFAULT_URL).read())
    token_count = len(tokens)
    msg = ''
    if token_count < 1 or tokens[0] in ['부분', 'ㅂㅂ', 'qq', 'ㅃ']:
        if user not in jdat:
            msg = '기억했던 내용이 없음. 사용법) !메모 <내용> [<메모가 들어갈 번호>]'
        else:
            div_idx = [None, None]
            if 1 < token_count and token_count < 4:
                for idx, token in enumerate(tokens[1:]):
                    div_idx[idx] = int(token) - (1 - idx)
            memo = jdat[user][div_idx[0]:div_idx[1]]
            indexed_memo = ['>*%3s' % (str(jdat[user].index(line) + 1) +
                            ':') + '* ' + line for line in memo]
            joined_memo = map(''.join, indexed_memo)
            msg = '\n'.join(joined_memo)
        return channel, msg
    if user not in jdat:
        jdat[user] = []
    line = len(jdat[user]) + 1
    if tokens[-1].isdigit() and token_count > 1:
        line = int(tokens[-1])
        tokens = tokens[:-1]
    contents = cat_token(tokens, 0)
    jdat[user].insert(line - 1, contents)
    with open(CACHE_DEFAULT_URL, 'w') as fp:
        json.dump(jdat, fp, indent=4)
    msg = '< '+contents+' > 을(를) 기억함.'
    return channel, msg
