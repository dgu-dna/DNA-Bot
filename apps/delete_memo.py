# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import isNumber
from time import localtime, strftime
import json
CACHE_DEFAULT_URL = './apps/memo_cache/memo_cache.json'


@on_command(['!메모삭제', '!ㅁㅁㅅㅈ', '!aatw'])
def run(robot, channel, tokens, user):
    '''메모 지워줌'''
    token_count = len(tokens)
    user = str(user)
    if token_count < 1:
        return channel, '사용법) !메모삭제 <메모 번호>'
    del_line = []
    for num in tokens:
        if(isNumber(num)):
            del_line.append(int(num))
    del_line.sort(reverse=True)
    jdat = json.loads(open(CACHE_DEFAULT_URL).read())
    if del_line[0] > len(jdat[user]):
        return channel, '그건 안댐;'
    for line in del_line:
        del jdat[user][line - 1]
    with open(CACHE_DEFAULT_URL, 'w') as fp:
        json.dump(jdat, fp, indent=4)
    del_line = map(lambda s: str(s), del_line)
    msg = '<' + ', '.join(sorted(del_line)) + '> 메모를 삭제 했음.'
    return channel, msg
