from apps.decorators import on_command
from apps.slackutils import is_koreanword
import json
import os
WORD_DEFAULT_URL = './apps/game_cache/relay.json'
CACHE_DEFAULT_URL = './apps/game_cache/relay_word.json'

@on_command(['!끝말', '!ㄲㅁ'])
def run(robot, channel, tokens, user, command):
    ''''''
    msg = '단어를 말해야...'
    if len(tokens) < 1:
        return channel, msg
    if len(tokens[0]) < 2:
        msg = '두 글자 이상의 단어만 가능함'
        return channel, msg
    if not is_koreanword(tokens[0]):
        msg = '단어가 아님'
        return channel, msg
    wdat = {}
    if os.path.exists(WORD_DEFAULT_URL):
        wdat = json.loads(open(WORD_DEFAULT_URL).read())
    if tokens[0] not in wdat:
        wdat[tokens[0]] = 0
    wdat[tokens[0]] += 1
    with open(WORD_DEFAULT_URL, 'w') as fp:
        json.dump(wdat, fp, indent=4)
    msg = ''
    game_info = {}
    word_info = json.loads(open(WORD_DEFAULT_URL).read())
    if os.path.exists(CACHE_DEFAULT_URL):
        game_info = json.loads(open(CACHE_DEFAULT_URL).read())
        if tokens[0] in game_info['used_word']:
            msg = '이미 썼던 단어임'
            return channel, msg
        if tokens[0][0] != game_info['start_word']:
            msg = '끝말잇기를 해야지!'
            return channel, msg
        game_info['used_word'].append(tokens[0])
    else:
        msg += '새로운 끝말잇기를 시작함\n'
        game_info['used_word'] = [tokens[0]]
    start_word = tokens[0][-1]
    my_word = ''
    for word in word_info.keys():
        if word[0] == start_word and word not in game_info['used_word']:
            game_info['used_word'].append(word)
            game_info['start_word'] = word[-1]
            my_word = word
            break
    with open(CACHE_DEFAULT_URL, 'w') as fp:
        json.dump(game_info, fp, indent=4)
    if my_word == '':
        msg += '내가 짐\n'
        os.remove(CACHE_DEFAULT_URL)
    else:
        msg += my_word
    return channel, msg
