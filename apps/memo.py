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
    if token_count < 1 or tokens[0] == '부분' or tokens[0] == 'ㅂㅂ' or tokens[0] == 'qq' or tokens[0] == 'ㅃ':
        if not os.path.isfile('/home/simneol/hongmoa/apps/memo_cache/'+str(user)):
            msg = '기억했던 내용이 없습니다. 사용법) !메모 <기억할 내용> [<메모가 들어갈 번호>]'
        else:
            f = open('/home/simneol/hongmoa/apps/memo_cache/'+str(user), 'r')
            start_num = -1
            end_num = -1
            if token_count >= 2:
                start_num = int(tokens[1])
            if token_count >= 3:
                end_num = int(tokens[2])
            line = f.readline()
            line_num = 0
            msg = ''
            if line:
                while line:
                    line_num += 1
                    if (start_num == -1 or line_num >= start_num) and (end_num == -1 or line_num <= end_num):
                        msg += '>*'+('%3s'%(str(line_num)+':'))+'* '+line
                    line = f.readline()
        return channel, msg
    contents = ''
    line = -1
    if tokens[-1].isdigit():
        line = int(tokens[-1])
        tokens = tokens[:-1]
    for s in tokens:
        contents += str(s)+' '
    #timestamp = strftime('%Y-%m-%d %H:%M:%S', localtime())
    data = contents[:-1]+'\n'#+' (Added at '+timestamp+')\n'
    insertLine('/home/simneol/hongmoa/apps/memo_cache/'+str(user), data, line)

    msg = '< '+contents[:-1]+' > 을(를) 기억했습니다.'
    return channel, msg


def insertLine(file, data, idx):
    with open(file, "r") as in_file:
        buf = in_file.readlines()
    with open(file, "w") as out_file:
        i = 0
        for line in buf:
            i += 1
            if i == idx:
                line = data + line
            out_file.write(line)
        if idx == -1:
            out_file.write(data)

if "__main__" == __name__:
    my = 12345
    msg = 'mymymy'
    msg = str(my)+msg
