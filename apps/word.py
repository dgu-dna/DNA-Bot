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
    msg = ''
    for token in tokens:
        if len(token) < 2:
            msg += '두 글자 이상의 단어만 가능함 (' + token + ')\n'
            continue
        if is_koreanword(token):
            wdat = {}
            if os.path.exists(CACHE_DEFAULT_URL):
                wdat = json.loads(open(CACHE_DEFAULT_URL).read())
            if token not in wdat:
                wdat[token] = 0
            wdat[token] += 1
            with open(CACHE_DEFAULT_URL, 'w') as fp:
                json.dump(wdat, fp, indent=4)
            msg += token + ' 은(는) 단어임\n'
        else:
            msg += token + ' 은(는) 단어가 아님\n'
    return channel, msg
