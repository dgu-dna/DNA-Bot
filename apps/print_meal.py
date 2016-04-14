#-*- coding: utf-8 -*-
from __future__ import unicode_literals
from decorators import on_command

import re
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
from time import localtime, strftime
def remove_html_tags(data):
    p=re.compile(r'<.*?>',re.M)
    #return p.findall(data)
    return p.sub('\n',data)

@on_command(['!밥','!학식', '!ㅎㅅ', '!gt'])
def run(robot, channel, tokens, user):
    '''오늘의 아리수, 상록원, 기숙사 학생식당의  메뉴를 보여줍니다\n
    !학식 [중식|ㅈㅅ|점심|wt|석식|ㅅㅅ|저녁|tt|ws]
    (옵션이 없을경우, 현재 시간에 맞는 메뉴가 보여집니다.)
    (상록원의 경우 메뉴가 없을경우 코너 순서가 다를 수 있습니다)
    '''
    html = urllib.urlopen('http://dgucoop.dongguk.ac.kr/store/store.php?w=4')
    soup = BeautifulSoup(html,'lxml')
    menus = soup.find_all('td',{'bgcolor':'#FFFFFF'})
    present_time=datetime.today()
    dinner_time=present_time.replace(hour=17,minute=0,second=0,microsecond=0)
    is_lunch=present_time<dinner_time
    if len(tokens)==1:
        if tokens[0] in set(['중식','ㅈㅅ','점심','wt']):
            is_lunch=True
        elif tokens[0] in set(['석식','ㅅㅅ','저녁','tt','ws']):
            is_lunch=False
    if is_lunch:
        message=':sunny:'+strftime('%m월 %d일(%a)',localtime())+'중식입니다 :sunny:\n'
        course=list([set([6,7,8,9]),set([20]),set([24])])
    else:
        message=':star2:'+strftime('%m월 %d일(%a)',localtime())+'석식입니다:star2:\n'
        course=list([set([10,11,12,13]),set([22]),set([27,28])])
    menu_num=0
    for menu in menus:
        menu_num+=1
        if menu_num == 6:
            message+='='*5+' 상록원(백반,일품,양식,뚝배기 순) '+'='*5+'\n'
        if menu_num == 20:
            message+='='*5+' 아리수 '+'='*5+'\n'
        if menu_num == 24:
            message+='='*5+' 남산학사 '+'='*5+'\n'
        for c in course:
            if menu_num in c:
                course_num=course.index(c)+1
                printed_num=0
                for line in remove_html_tags(str(menu)).split('\n'):
                    if line.rstrip() and printed_num < course_num:
                        printed_num+=1
                        message += line
                        if menu_num<20 and menu_num % 4 != 1:
                            message += ' || '
                        else:
                            message += '\n'
    return channel, message

if "__main__" == __name__:
    html = urllib.urlopen('http://dgucoop.dongguk.ac.kr/store/store.php?w=4')
    soup = BeautifulSoup(html,'lxml')
    all_ = soup.find_all('div',{'id':'sdetail'})
    stores = soup.find_all('td',{'class':'menu_st'})
    menus = soup.find_all('td',{'bgcolor':'#FFFFFF'})
    menu_num=0
    present_time=datetime.today()
    dinner_time=present_time.replace(hour=17,minute=0,second=0,microsecond=0)
    print present_time
    print dinner_time
    print present_time<dinner_time

    course=list([set([6,7,8,9]),set([20]),set([24,25])])
    message=''
    menu_num=0
    for menu in menus:
        menu_num+=1
        if menu_num == 6:
            message+='='*5+' 상록원(백반,일품,양식,뚝배기 순) '+'='*5+'\n'
        if menu_num == 20:
            message+='='*5+' 아리수 '+'='*5+'\n'
        if menu_num == 24:
            message+='='*5+' 남산학사 '+'='*5+'\n'
        for c in course:
            if menu_num in c:
                course_num=course.index(c)+1
                printed_num=0
                for line in remove_html_tags(str(menu)).split('\n'):
                    if line.rstrip() and printed_num < course_num:
                        printed_num+=1
                        message += line +'\n'
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
