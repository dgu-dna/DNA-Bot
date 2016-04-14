#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from time import localtime, strftime

def isNum(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

@on_command(['!메모삭제', '!ㅁㅁㅅㅈ', '!aatw'])
def run(robot, channel, tokens, user):
    '''메모한 내용을 삭제합니다.\n
    !메모삭제 <메모 번호>
    '''
    token_count = len(tokens)
    msg=''
    if token_count < 1:
        return channel, '사용법) !메모삭제 <메모 번호>'
    del_line=list()
    for num in tokens:
        if(isNum(num)):
            del_line.append(int(num))
    f=open('/home/simneol/hongmoa/apps/memo_cache/'+str(user),'r')
    line_num=0
    contents=''
    line=f.readline()
    if line:
        while line:
            line_num+=1
            if line_num not in del_line:
                contents+=line
            line=f.readline()
    f.close()
    del_line.sort()
    maxnum=del_line.pop()
    if maxnum>line_num:
        return channel, ':smile_cat: Exception : Index Out of Range :smile_cat:'
    del_line.append(maxnum)
    f = open('/home/simneol/hongmoa/apps/memo_cache/'+str(user),'w')
    f.write(contents)
    msg = '<'
    for num in del_line:
        msg+=str(num)+','
    msg=msg[:-1]+'> 메모를 삭제 했습니다.'
    return channel, msg

if "__main__"==__name__:
    msg=''
    msg+=strftime('%Y-%m-%d %H:%M:%S',localtime())
    print msg
