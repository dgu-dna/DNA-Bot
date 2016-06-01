from apps.decorators import on_command
from apps.slackutils import is_koreanword
import random
import json
import os
WORD_DEFAULT_URL = './apps/game_cache/relay.json'
CACHE_DEFAULT_URL = './apps/game_cache/relay_word.json'


def get_startword(word):
    start_word = [word[-1]]
    ch = ord(word[-1]) - 0xAC00
    choseong = ch // (21 * 28)
    if choseong == 5:
        start_word.append(chr(ch + 0xAC00 - 3*21*28))
    ch = ord(start_word[-1]) - 0xAC00
    choseong = ch // (21*28)
    jungseong = ch % (21*28) // 28
    if choseong == 2 and jungseong in [2, 6, 12, 17, 20]:
        start_word.append(chr(ch + 0xAC00 + 9*21*28))
    return start_word


@on_command(['!끝말', '!ㄲㅁ'])
def run(robot, channel, tokens, user, command):
    ''''''
    msg = '단어를 말해야...'
    if len(tokens) < 1:
        return channel, msg
    if len(tokens[0]) < 2:
        msg = '두 글자 이상의 단어만 가능함'
        return channel, msg
    if tokens[0] == '포기할래':
        if os.path.exists(CACHE_DEFAULT_URL):
            os.remove(CACHE_DEFAULT_URL)
            msg = 'ㅎㅎ 내가이김'
            return channel, msg
        else:
            msg = '시작한것도 없음'
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
        if tokens[0][0] not in game_info['start_word']:
            msg = '끝말잇기를 해야지! (현재 단어: ' + game_info['last_word'] + ')'
            return channel, msg
        game_info['used_word'].append(tokens[0])
    else:
        msg += '새로운 끝말잇기를 시작함\n'
        game_info['used_word'] = [tokens[0]]
    start_word = get_startword(tokens[0])
    candidate_word = []
    my_word = ''
    for word in word_info.keys():
        if word[0] in start_word and word not in game_info['used_word']:
            for i in range(word_info[word]):
                candidate_word.append(word)
    if candidate_word:
        print(candidate_word)
        my_word = random.choice(candidate_word)
        game_info['last_word'] = my_word
        game_info['used_word'].append(my_word)
        game_info['start_word'] = get_startword(my_word)
        with open(CACHE_DEFAULT_URL, 'w') as fp:
            json.dump(game_info, fp, indent=4)
        msg += my_word
    else:
        msg += '내가 짐\n'
        if os.path.exists(CACHE_DEFAULT_URL):
            os.remove(CACHE_DEFAULT_URL)
    return channel, msg
