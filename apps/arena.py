from apps.decorators import on_command
from apps.slackutils import send_msg, get_nickname
from urllib.request import urlopen, quote
from subprocess import check_output, CalledProcessError, STDOUT
import os
import re
import json
import time
import shutil
CACHE_DEFAULT_URL = './apps/request_cache/'
SOURCE_DEFAULT_URL = './apps/arena_cache/'


def battle(user1, user2):
    msg = ''
    good_status = True
    gm_f = open(SOURCE_DEFAULT_URL + 'GameManager.h', encoding='ISO-8859-1').read()
    gm_f = re.sub('%P1%', user1, gm_f)
    gm_f = re.sub('%P2%', user2, gm_f)
    with open(SOURCE_DEFAULT_URL + '/prog/GameManager.h', 'w', encoding='ISO-8859-1') as fp:
        fp.write(gm_f)
    shutil.copy(SOURCE_DEFAULT_URL + user1 + '.cpp', SOURCE_DEFAULT_URL + 'prog/')
    shutil.copy(SOURCE_DEFAULT_URL + user1 + '.h', SOURCE_DEFAULT_URL + 'prog/')
    shutil.copy(SOURCE_DEFAULT_URL + user2 + '.cpp', SOURCE_DEFAULT_URL + 'prog/')
    shutil.copy(SOURCE_DEFAULT_URL + user2 + '.h', SOURCE_DEFAULT_URL + 'prog/')
    try:
        msg += check_output(['/bin/bash', '-c', 'g++ -std=c++11 ' + SOURCE_DEFAULT_URL + 'prog/*.cpp -o ' + user1 + user2], stderr=STDOUT).decode('utf-8')
    except CalledProcessError as e:
        msg += e.output.decode('utf-8')
        msg += '\n컴파일 에러...'
        os.remove(SOURCE_DEFAULT_URL + 'prog/' + user1 + '.cpp')
        os.remove(SOURCE_DEFAULT_URL + 'prog/' + user1 + '.h')
        os.remove(SOURCE_DEFAULT_URL + 'prog/' + user2 + '.cpp')
        os.remove(SOURCE_DEFAULT_URL + 'prog/' + user2 + '.h')
        good_status = False
        return msg, good_status
    os.remove(SOURCE_DEFAULT_URL + 'prog/' + user1 + '.cpp')
    os.remove(SOURCE_DEFAULT_URL + 'prog/' + user1 + '.h')
    os.remove(SOURCE_DEFAULT_URL + 'prog/' + user2 + '.cpp')
    os.remove(SOURCE_DEFAULT_URL + 'prog/' + user2 + '.h')
    try:
        msg += check_output(['./' + user1 + user2]).decode('utf-8')
    except CalledProcessError as e:
        msg += e.output.decode('utf-8')
        msg += '\n런타임 에러...'
        good_status = False
    os.remove('./' + user1 + user2)
    return msg, good_status


@on_command(['!대전'])
def run(robot, channel, tokens, user, command):
    ''''''
    ttl = 0
    msg = ''
    req = {}
    req['type'] = 'message'
    req['channel'] = channel
    req['user'] = user
    info = json.loads(open(SOURCE_DEFAULT_URL + 'userinfo.json').read())
    if len(tokens) < 1:
        msg = '사용법 오류 `!대전 등록`, `!대전 @Name`'
        return channel, msg
    if tokens[0] == '등록':
        if channel[0] == 'C':
            msg = '채널에선 불가함! 나한테 직접 1:1 대화를 걸어서 진행하셈!'
            return channel, msg
        info = json.loads(open(SOURCE_DEFAULT_URL + 'userinfo.json').read())
        if user in info:
            msg = '이미 등록했던 소스가 있음! 다시 등록절차를 진행하면 덮어쓰기 되는데 괜찮음? [네/아니오]'
            send_msg(robot, channel, msg)
            ttl = 30
            with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                json.dump(req, fp, indent=4)
            while True:
                time.sleep(1)
                ttl -= 1
                if ttl == 0:
                    return channel, '시간 초과. 처음부터 다시 진행하셈'
                if os.path.exists(CACHE_DEFAULT_URL + 'ARENA'):
                    e = json.loads(open(CACHE_DEFAULT_URL + 'ARENA').read())
                    os.remove(CACHE_DEFAULT_URL + 'ARENA')
                    e = e[0]
                    if e['text'] == '네':
                        break
                    if e['text'] == '아니오':
                        msg = '등록 절차를 중단함'
                        return channel, msg
                    with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                        json.dump(req, fp, indent=4)
        source = ''
        name = ''
        ssn_check = re.compile(r'[\r\n.]*(M[0-9]{10}.h)[\r\n.]*')
        ttl = 30
        with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
            json.dump(req, fp, indent=4)
        send_msg(robot, channel, '헤더 말고 소스(.cpp)만 텍스트로 복붙해서 올려!! 다 올리면 "끝" 이라고 외쳐!')
        while True:
            time.sleep(1)
            ttl -= 1
            if ttl == 0:
                return channel, '시간 초과. 처음부터 다시 진행하셈'
            if os.path.exists(CACHE_DEFAULT_URL + 'ARENA'):
                ttl = 30
                e = json.loads(open(CACHE_DEFAULT_URL + 'ARENA').read())
                os.remove(CACHE_DEFAULT_URL + 'ARENA')
                e = e[0]
                if e['text'] == '끝':
                    ssn_list = ssn_check.findall(source)
                    if ssn_list:
                        name = ssn_list[0][:-2]
                        for key, value in info.items():
                            if value['ssn'] == name and key != user:
                                return channel, '이미 등록된 학번인데....?'
                    else:
                        return channel, '소스에서 학번을 찾을 수 없는데...?'
                    source = re.sub('&amp;', '&', source)
                    source = re.sub('&lt;', '<', source)
                    source = re.sub('&gt;', '>', source)
                    with open(SOURCE_DEFAULT_URL + name + '.cpp', 'w') as fp:
                        fp.write(source)
                    break
                source += e['text'] + '\n'
                with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                    json.dump(req, fp, indent=4)

        source = ''
        ttl = 30
        with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
            json.dump(req, fp, indent=4)
        send_msg(robot, channel, '마찬가지로 헤더도 복붙해서 올려!! 다 올리면 "끝" 이라고 외쳐!')
        while True:
            time.sleep(1)
            ttl -= 1
            if ttl == 0 :
                return channel, '시간 초과. 처음부터 다시 진행하셈'
            if os.path.exists(CACHE_DEFAULT_URL + 'ARENA'):
                ttl = 30
                e = json.loads(open(CACHE_DEFAULT_URL + 'ARENA').read())
                os.remove(CACHE_DEFAULT_URL + 'ARENA')
                e = e[0]
                if e['text'] == '끝':
                    source = re.sub('&amp;', '&', source)
                    source = re.sub('&lt;', '<', source)
                    source = re.sub('&gt;', '>', source)
                    with open(SOURCE_DEFAULT_URL + name + '.h', 'w') as fp:
                        fp.write(source)
                    break
                source += e['text'] + '\n'
                with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                    json.dump(req, fp, indent=4)
        send_msg(robot, channel, '유효성 검사를 위해, 랜덤봇과 테스트를 진행한다! 이 작업은 최대 10초 정도 걸린다!')
        msg, is_good = battle('Assistant', name)
        if not is_good:
            del info[user]
            with open(SOURCE_DEFAULT_URL + 'userinfo.json', 'w') as fp:
                json.dump(info, fp, indent=4)
            os.remove(SOURCE_DEFAULT_URL + name + '.cpp')
            os.remove(SOURCE_DEFAULT_URL + name + '.h')
            msg += '\n 소스코드의 상태가....? (기존 소스코드 삭제됨)'
            return channel, msg
        msg = '좋아 합격!\n\n'
        user_info = {}
        user_info['ssn'] = name
        msg += '''다른 사람이 너의 소스파일과 대전하고 싶을때,
너의 허락을 맡지않고도 대전시킬 수 있게 하겠니? [네/아니오]'''
        send_msg(robot, channel, msg)
        ttl = 30
        with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
            json.dump(req, fp, indent=4)
        while True:
            time.sleep(1)
            ttl -= 1
            if ttl == 0:
                return channel, '시간 초과. 처음부터 다시 진행하셈'
            if os.path.exists(CACHE_DEFAULT_URL + 'ARENA'):
                e = json.loads(open(CACHE_DEFAULT_URL + 'ARENA').read())
                os.remove(CACHE_DEFAULT_URL + 'ARENA')
                e = e[0]
                if e['text'] == '네':
                    user_info['battle_when_absence'] = True
                    break
                if e['text'] == '아니오':
                    user_info['battle_when_absence'] = False
                    user_info['notify_result'] = False
                    break
                with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                    json.dump(req, fp, indent=4)
        if user_info['battle_when_absence']:
            msg = '''그러면 그렇게 진행된 대전 결과를 모두 1:1대화로 따로 알려줄까? [네/아니오]'''
            send_msg(robot, channel, msg)
            ttl = 30
            with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                json.dump(req, fp, indent=4)
            while True:
                time.sleep(1)
                ttl -= 1
                if ttl == 0:
                    return channel, '시간 초과. 처음부터 다시 진행하셈'
                if os.path.exists(CACHE_DEFAULT_URL + 'ARENA'):
                    e = json.loads(open(CACHE_DEFAULT_URL + 'ARENA').read())
                    os.remove(CACHE_DEFAULT_URL + 'ARENA')
                    e = e[0]
                    if e['text'] == '네':
                        user_info['notify_result'] = True
                        break
                    if e['text'] == '아니오':
                        user_info['notify_result'] = False
                        break
                    with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                        json.dump(req, fp, indent=4)
        info[user] = user_info
        with open(SOURCE_DEFAULT_URL + 'userinfo.json', 'w') as fp:
            json.dump(info, fp, indent=4)
        msg = 'OK. Code 정상 등록 완료. 이제 다른 사람과 `!대전 @user` 명령어를 통해 대전할 수 있다!'
    if tokens[0][:2] == '<@':
        if channel[0] == 'D':
            return channel, 'DM에선 불가능!'
        user2 = tokens[0][2:-1]
        if user == user2:
            return channel, '자기 자신과는 불가능!'
        user2_presence = False
        result = robot.client.api_call('channels.info', channel='C0SNZ83TK')
        if user2 not in result['channel']['members']:
            return channel, '상대방이 이 채널에 없음!'
        if user not in info:
            msg = '소스등록부터 먼저 하고 하셈! `!대전 등록`'
            return channel, msg
        if user2 not in info:
            msg = '상대방이 소스등록을 안했음! `!대전 등록`'
            return channel, msg
        if not info[user2]['battle_when_absence']:
            user2_presence = True
            send_msg(robot, channel, '상대방의 의사를 묻겠음! [ㄱㄱ/ㄴㄴ]')
            req['user'] = user2
            ttl = 30
            with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                json.dump(req, fp, indent=4)
            while True:
                time.sleep(1)
                ttl -= 1
                if ttl == 0:
                    return channel, '시간 초과. 처음부터 다시 진행하셈'
                if os.path.exists(CACHE_DEFAULT_URL + 'ARENA'):
                    e = json.loads(open(CACHE_DEFAULT_URL + 'ARENA').read())
                    os.remove(CACHE_DEFAULT_URL + 'ARENA')
                    e = e[0]
                    if e['text'] == 'ㄱㄱ':
                        break
                    if e['text'] == 'ㄴㄴ':
                        msg = '상대방이 거부함!'
                        return channel, msg
                    with open(CACHE_DEFAULT_URL + 'REQUEST_ARENA.req', 'w') as fp:
                        json.dump(req, fp, indent=4)
        msg += 'Player 1 : <@' + user + '>\n'
        msg += '                 VS\n'
        msg += 'Player 2 : <@' + user2 + '>\n\n'
        prev_msg = msg
        msg += '대전 시작 !!!'
        send_msg(robot, channel, msg)
        msg = '======== 결과 ========\n'
        result, is_good = battle(info[user]['ssn'], info[user2]['ssn'])
        msg += result
        if info[user2]['notify_result'] and user2_presence == False:
            result = robot.client.api_call('im.open', user=user2)
            send_msg(robot, result['channel']['id'], prev_msg + '\n' + msg)
    return channel, msg
