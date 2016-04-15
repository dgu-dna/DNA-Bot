# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command

import re
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
from time import localtime, strftime


def remove_html_tags(data):
    p = re.compile(r'<.*?>', re.M)
    # return p.findall(data)
    return p.sub('\n', data)


@on_command(['!밥', '!학식', '!ㅎㅅ', '!gt'])
def run(robot, channel, tokens, user):
    '''학식 메뉴'''
    print "this is debug msg"
    html = urllib.urlopen('http://dgucoop.dongguk.ac.kr/store/store.php?w=4')
    soup = BeautifulSoup(html, 'lxml')
    menus = soup.find_all(True, {'bgcolor': '#FFFFFF'})
    present_time = datetime.today()
    dinner_time = present_time.replace(hour=17, minute=0, second=0, microsecond=0)
    is_lunch = present_time < dinner_time
    if len(tokens) == 1:
        if tokens[0] in set(['중식', 'ㅈㅅ', '점심', 'wt']):
            is_lunch = True
        elif tokens[0] in set(['석식', 'ㅅㅅ', '저녁', 'tt', 'ws']):
            is_lunch = False
    if is_lunch:
        message = ':sunny:'+strftime('%m월 %d일(%a)', localtime())+'중식입니다 :sunny:\n'
        course = list([list([6, 7, 8, 9]), list([22]), list([26])])
    else:
        message = ':star2:'+strftime('%m월 %d일(%a)', localtime())+'석식입니다:star2:\n'
        course = list([list([10, 11, 12, 13]), list([24]), list([29, 30])])
    menu_num = 0
    pannoodle_num = 20
    for menu in menus:
        menu_num += 1
        if menu_num == course[0][0]:
            message += '='*5+' 상록원 '+'='*5+'\n'
        if menu_num == course[1][0]:
            message = message[:-4] + '\n' + '='*5+' 아리수 '+'='*5+'\n'
        if menu_num == course[2][0]:
            message += '='*5+' 남산학사 '+'='*5+'\n'
        for c in course:
            if menu_num == 16:
                m=''
                for line in remove_html_tags(str(menu)).split('\n'):
                    m += line
                if m == '휴무':
                    pannoodle_num -= 1
                    for idx, val in enumerate(c):
                        if c[idx] > 16:
                            c[idx] -= 3
                    continue
            if menu_num == pannoodle_num:
                m=''
                for line in remove_html_tags(str(menu)).split('\n'):
                    m += line
                if m == '휴무':
                    for idx, val in enumerate(c):
                        if c[idx] > pannoodle_num:
                            c[idx] -= 1
                    continue
            if menu_num in c:
                course_num = course.index(c)+1
                printed_num = 0
                for line in remove_html_tags(str(menu)).split('\n'):
                    if line.rstrip() and printed_num < course_num:
                        printed_num += 1
                        message += line
                        s_course=['양', '뚝', '백', '일']
                        if menu_num < 20 :
                            message += '('+s_course[menu_num%4]+')'
                            message += ' || '
                        else:
                            message += '\n'
    return channel, message

if "__main__" == __name__:
    html = urllib.urlopen('http://dgucoop.dongguk.ac.kr/store/store.php?w=4')
    soup = BeautifulSoup(html, 'lxml')
    all_ = soup.find_all('div', {'id': 'sdetail'})
    stores = soup.find_all('td', {'class': 'menu_st'})
    menus = soup.find_all(True, {'bgcolor': '#FFFFFF'})
    menu_num = 0
    present_time = datetime.today()
    dinner_time = present_time.replace(hour=17, minute=0, second=0, microsecond=0)
    print present_time
    print dinner_time
    print present_time < dinner_time

    course = list([set([6, 7, 8, 9]), set([20]), set([24, 25])])
    message = ''
    mymessage=''
    menu_num = 0
    for menu in menus:
        menu_num += 1
        if menu_num == 6:
            message += '='*5+' 상록원(백반,일품,양식,뚝배기 순) '+'='*5+'\n'
        if menu_num == 20:
            message += '='*5+' 아리수 '+'='*5+'\n'
        if menu_num == 24:
            message += '='*5+' 남산학사 '+'='*5+'\n'
        for c in course:
            if menu_num < 27:
                mymessage +=  '\n :: ' + str(menu_num) + ' :: \n '
                for line in remove_html_tags(str(menu)).split('\n'):
                    mymessage += line
                break
            if menu_num == 27:
                print mymessage
                menu_num = 50
                break
            if menu_num in c:
                course_num = course.index(c)+1
                printed_num = 0
                for line in remove_html_tags(str(menu)).split('\n'):
                    if line.rstrip() and printed_num < course_num:
                        printed_num += 1
                        message += line+'\n'
    print message

#    mm=''
#    for menu in menus:
#        menu_num+=1
#        if menu_num==6:
#            course=0
#            for al in remove_html_tags(str(menu)).split('\n'):
#                if al.rstrip() and course < 2:
#                    print al
#                    break

#    for menu in menus:
#        menu_num+=1
#        for line in remove_html_tags(str(menu)).split('\n'):
#            if line.rstrip() and menu_num == 20:
#                print line
# meals = tables[0]
# for meal in tables:
#     print meal
# for table in tables:
#    meals = table[0]
