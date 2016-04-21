# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
from time import localtime, strftime


def remove_html_tags(data):
    p = re.compile(r'<.*?>', re.M)
    # return p.findall(data)
    #return p.sub('\n', data)
    return data

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
