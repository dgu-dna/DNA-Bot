#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command
from time import localtime, strftime
import json, urllib, os
from subprocess import check_output

@on_command(['기억','ㄱㅇ','rd'])
def run(robot, channel, tokens, user):
    '''어떠한 단어에 대한 설명을 기억합니다.
    !기억 <기억할단어> <기억할 문장>
    기억했던 모든 단어는 "!기억 ?"를 입력 시 출력합니다.'''
    url='https://slack.com/api/users.info?token=xoxp-26726533763-26813510823-33040779782-4d90d5301c&user='+str(user)+'&pretty=1'
    response = urllib.urlopen(url)
    data=json.loads(response.read())
    if os.path.exists('/home/simneol/hongmoa/apps/name_cache/'+str(tokens[0])):
        f=open('/home/simneol/hongmoa/apps/name_cache/'+str(tokens[0]),'r')
    else:
        f=None
    full_line=''
    if len(tokens)<2:
        if str(tokens[0]) == '?':
            all_file=check_output(['ls','/home/simneol/hongmoa/apps/name_cache/'])
            msg = '제가 여태까지 기억한 것들은 아래와 같아요!\n'
            for s in all_file.split('\n'):
                msg+=s+' || '
            msg = msg[:-8]
            return channel, msg
        if not f:
            msg=str(tokens[0])+'에 대해 기억나는게 없어요 ㅠㅡㅠ'
            return channel, msg
        time = line = f.readline()
        while line:
            line=f.readline()
            full_line+=line
        msg=full_line+'\n'+time
    else:
        if f:
            line = f.readline()
            while line:
                line=f.readline()
                full_line+=line
        full_line='가장 최근에 '+str(data['user']['name'])[:1]+'·'+str(data['user']['name'])[1:]+'이(가) '+strftime('%Y-%m-%d %H:%M:%S',localtime())+'에 알려줬어요!\n'+full_line
        desc=''
        for i in range(1,len(tokens)):
            desc+=tokens[i]+' '
        full_line=full_line+desc[:-1]+'\n'
        if f:
            f.close()
        f=open('/home/simneol/hongmoa/apps/name_cache/'+str(tokens[0]),'w')
        f.write(full_line)
        msg = str(tokens[0])+'에 대해 '+desc[:-1]+'(이)라고 기억했어요!'

#    msg = str(data['user']['name'])+'이(가) '+strftime('%Y-%m-%d %H:%M:%S',localtime())+'에 불러주었어요!'
    return channel, msg

if "__main__"==__name__:
    url='https://slack.com/api/users.info?token=xoxp-26726533763-26813510823-33040779782-4d90d5301c&user=U0SPF91EE&pretty=1'
    response = urllib.urlopen(url)
    data=json.loads(response.read())
    print data['user']['name']
