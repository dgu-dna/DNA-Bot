from apps.decorators import on_command
from bs4 import BeautifulSoup
from urllib.request import urlopen, quote
import json
import re
CACHE_DEFAULT_URL = './apps/game_cache/relay.json'
NAVER_DICTIONARY_URL = 'http://krdic.naver.com/search.nhn?query=%s&kind=keyword'


@on_command(['!단어'])
def run(robot, channel, tokens, user, command):
    ''''''
    msg = '단어를 말해줘야 하지'
    is_word = False
    if len(tokens) < 1:
        return channel, msg
    html = urlopen(quote((NAVER_DICTIONARY_URL % tokens[0]).encode('utf-8'), '/:&?='))
    if len(tokens[0]) < 2:
        msg = '두 글자 이상의 단어만 가능함'
        return channel, msg
    soup = BeautifulSoup(html, 'html.parser')
    s = soup.find_all('a', {'class': 'fnt15'})
    if s:
        for ss in s:
            if re.sub(r'[^가-힣]', '', str(ss)) == tokens[0]:
                is_word = True
                break
    #for ss in s:
    #    print(re.sub(r'[^ㄱ-ㅎ가-힣]', '', str(ss)))
    #print(s)
    #print(soup.find_all('ul', {'class': 'lst3'})[0].find_all('li'))
    if is_word:
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

