from apps.decorators import on_command
from apps.slackutils import is_koreanword, get_nickname, get_realname
import random
import json
import os
WORD_DEFAULT_URL = './apps/game_cache/relay.json'
CACHE_DEFAULT_URL = './apps/game_cache/relay_word.json'
RANK_DEFAULT_URL = './apps/game_cache/rank.json'

def save_rank(user, score):
    rdat = {}
    if os.path.exists(RANK_DEFAULT_URL):
        rdat = json.loads(open(RANK_DEFAULT_URL).read())
    if user in rdat:
        if 'relay_word' in rdat[user]:
            if rdat[user]['relay_word'] < score:
                rdat[user]['relay_word'] = score
        else:
            rdat[user]['relay_word'] = score
    else:
        rdat[user] = {'relay_word': score}
    with open(RANK_DEFAULT_URL, 'w') as fp:
        json.dump(rdat, fp, indent=4)

def get_highest_rank():
    score = -1
    name = None
    if os.path.exists(RANK_DEFAULT_URL):
        rdat = json.loads(open(RANK_DEFAULT_URL).read())
        if rdat:
            for user in rdat.keys():
                if 'relay_word' in rdat[user]:
                    if rdat[user]['relay_word'] > score:
                        score = rdat[user]['relay_word']
                        if user == 'bot':
                            name = '승규'
                        else:
                            name = get_realname(user)
                    #if rdat[user]['relay_word'] == score:
    return name, score


def add_score(user, jsdat):
    if 'user' not in jsdat:
        jsdat['user'] = {}
    if user in jsdat['user']:
        jsdat['user'][user] += 1
    else:
        jsdat['user'][user] = 1


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
    json_file = CACHE_DEFAULT_URL + '_' + channel
    msg = '단어를 말해야...'
    if len(tokens) < 1:
        return channel, msg
    if len(tokens[0]) < 2:
        msg = '두 글자 이상의 단어만 가능함'
        return channel, msg
    if tokens[0] == '포기할래':
        if os.path.exists(json_file):
            game_info = json.loads(open(json_file).read())
            score = game_info['score']
            os.remove(json_file)
            save_rank('bot', score)
            msg = 'ㅎㅎ 내가이김. (승규의 점수: ' + str(score) + ')\n'
            rank_msg = '\n'
            if 'user' in game_info:
                for user, score in game_info['user'].items():
                    rank_msg += get_nickname(user) + ' : ' + str(score) + '점\n'
            rank_msg += '(패배시에는 점수가 반영되지 않음)\n'
            top_name, top_score = get_highest_rank()
            if top_name:
                msg += '> :crown: 끝말잇기의 달인 : ' + top_name + ' (' + str(top_score) + '점)'
            msg += rank_msg
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
    if os.path.exists(json_file):
        game_info = json.loads(open(json_file).read())
        if tokens[0] in game_info['used_word']:
            msg = '이미 썼던 단어임'
            return channel, msg
        if tokens[0][0] not in game_info['start_word']:
            msg = '끝말잇기를 해야지! (현재 단어: ' + game_info['last_word'] + ')'
            return channel, msg
        add_score(user, game_info)
        game_info['used_word'].append(tokens[0])
    else:
        msg += '새로운 끝말잇기를 시작함\n'
        add_score(user, game_info)
        game_info['used_word'] = [tokens[0]]
    start_word = get_startword(tokens[0])
    candidate_word = []
    my_word = ''
    for word in word_info.keys():
        if word[0] in start_word and word not in game_info['used_word']:
            for i in range(word_info[word]):
                candidate_word.append(word)
    if candidate_word:
        my_word = random.choice(candidate_word)
        game_info['last_word'] = my_word
        game_info['used_word'].append(my_word)
        game_info['start_word'] = get_startword(my_word)
        if 'score' in game_info:
            game_info['score'] += 1
        else:
            game_info['score'] = 1
        with open(json_file, 'w') as fp:
            json.dump(game_info, fp, indent=4)
        msg += my_word
    else:
        msg += '내가 짐.\n'
        rank_msg = '\n'
        if 'user' in game_info:
            for user, score in game_info['user'].items():
                rank_msg += get_nickname(user) + ' : ' + str(score) + '점\n'
                save_rank(user, score)
        top_name, top_score = get_highest_rank()
        if top_name:
            msg += '> :crown: 끝말잇기의 달인 : ' + top_name + ' (' + str(top_score) + '점)'
        msg += rank_msg
        if os.path.exists(json_file):
            os.remove(json_file)
    return channel, msg
