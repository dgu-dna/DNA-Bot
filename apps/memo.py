# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from time import localtime, strftime
import os

@on_command(['!메모', '!ㅁㅁ', '!aa'])
def run(robot, channel, tokens, user):
    '''메모 기억해드림'''
    token_count = len(tokens)
    msg = ''
    if token_count < 1:
        if not os.path.isfile('/home/simneol/hongmoa/apps/memo_cache/'+str(user)):
            msg = '기억했던 내용이 없습니다. 사용법) !메모 <기억할 내용>'
        else:
            f = open('/home/simneol/hongmoa/apps/memo_cache/'+str(user), 'r')
            line = f.readline()
            line_num = 0
            if line:
                while line:
                    line_num += 1
                    msg += str(line_num)+': '+line
                    line = f.readline()
                msg = '='*14+'총 '+str(line_num)+'개 있음'+'='*14+'\n'+msg
        return channel, msg
    contents = ''
    for s in tokens:
        contents += str(s)+' '
    f = open('/home/simneol/hongmoa/apps/memo_cache/'+str(user), 'a')
    timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime())
    f.write(contents[:-1]+' (Added at '+timestamp+')\n')
    msg = '<'+contents[:-1]+'> 을(를) 기억했습니다.'
    return channel, msg

if "__main__" == __name__:
    my = 12345
    msg = 'mymymy'
    msg = str(my)+msg
