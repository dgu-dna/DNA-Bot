from apps.decorators import on_command
from apps.slackutils import is_koreanword
import json
import os
import re
CACHE_DEFAULT_URL = './apps/game_cache/relay.json'


@on_command(['!단어'])
def run(robot, channel, tokens, user, command):
    ''''''
    msg = '단어를 말해줘야 하지'
    if len(tokens) < 1:
        return channel, msg
    if len(tokens[0]) < 2:
        msg = '두 글자 이상의 단어만 가능함'
        return channel, msg
    if is_koreanword(tokens[0]):
        wdat = {}
        if os.path.exists(CACHE_DEFAULT_URL):
            wdat = json.loads(open(CACHE_DEFAULT_URL).read())
        if tokens[0] not in wdat:
            wdat[tokens[0]] = 0
        wdat[tokens[0]] += 1
        with open(CACHE_DEFAULT_URL, 'w') as fp:
            json.dump(wdat, fp, indent=4)
        msg = tokens[0] + ' 은(는) 단어임'
    else:
        msg = tokens[0] + ' 은(는) 단어가 아님'
    return channel, msg
