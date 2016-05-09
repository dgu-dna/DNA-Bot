# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
import re
import copy
import urllib
from bs4 import BeautifulSoup
from datetime import datetime
from time import localtime, strftime

DGUCOOP_URL = 'http://dgucoop.dongguk.ac.kr/store/store.php?w=4'
ORIGINAL_INFO = {
                    0:
                    {
                        'name': '교직원',
                        'cnt': 4,
                        'details': ['집밥', '한그릇', '채식당'],
                        'dinner_cnt': [3, 3, 0]
                    },
                    5:
                    {
                        'name': '상록원',
                        'cnt': 7,
                        'details': ['백반', '일품', '양식', '뚝배기'],
                        'dinner_cnt': [4, 4, 4, 4]
                    },
                    15:
                    {
                        'name': '그루터기',
                        'cnt': 3,
                        'details': ['A코너', 'B코너'],
                        'dinner_cnt': [2, 2]
                    },
                    19:
                    {
                        'name': '팬앤누들',
                        'cnt': 1,
                        'details': ['Pan', 'Noodle'],
                        'dinner_cnt': [0, 0]
                    },
                    21:
                    {
                        'name': '아리수',
                        'cnt': 2,
                        'details': ['메뉴', '분식'],
                        'dinner_cnt': [2, 0]
                    },
                    25:
                    {
                        'name': '남산학사',
                        'cnt': 5,
                        'details': ['A코너', 'B코너', '푸드코트'],
                        'dinner_cnt': [3, 3, 0]
                    }
                }


def remove_noise(data):
    # Delete HTML tag
    a = re.sub(r'<.*?>', '', data)
    # Delete Blank line
    b = re.sub(r'(^|\n)\s*\n', r'\1', a)
    # Delete Price tag
    c = re.sub(r'\s*:?￦?[0-9],?[0-9]{3}원?.*$', '', b, flags=re.M)
    # Delete source tag (min)
    d = re.sub(r'\(.*(국내|스페인|독일|호주|베트남|러시아)산.*\)', '', c, flags=re.M)
    # Delete source tag (all)
    e = re.sub(r'^.*(국내|스페인|독일|호주|베트남|러시아)산.*$', '', d, flags=re.M)
    # Delete Blank line
    f = re.sub(r'\n\s*$', '', e)
    return f


@on_command(['!밥', '!학식', '!ㅎㅅ', '!gt'])
def run(robot, channel, tokens, user):
    '''학식 메뉴보여줌'''
    COURSE_INFO = copy.deepcopy(ORIGINAL_INFO)
    now_t = datetime.today().time()
    course = {}
    print_course = ['상록원', '아리수', '남산학사']   # default
    is_lunch = now_t < now_t.replace(17, 0, 0, 0)   # dinner
    full_print = False
    if len(tokens) > 0:
        for token in tokens:
            if token in ['중식', 'ㅈㅅ', '점심', 'wt']:
                is_lunch = True
            elif token in ['석식', 'ㅅㅅ', '저녁', 'tt', 'ws']:
                is_lunch = False
            else:
                print_course = []
        for token in tokens:
            if token in ['교직원식당', '교', 'ㄱ', 'r']:
                if '교직원' not in print_course:
                    print_course.append('교직원')
            elif token in ['팬앤누들', '팬', 'ㅍ', 'v']:
                if '팬앤누들' not in print_course:
                    print_course.append('팬앤누들')
            elif token in ['상록원', '상', 'ㅅ', 't']:
                if '상록원' not in print_course:
                    print_course.append('상록원')
            elif token in ['아리수', '아', 'ㅇ', 'd']:
                if '아리수' not in print_course:
                    print_course.append('아리수')
            elif token in ['남산학사', '긱식', '남', '긱', '기', 's']:
                if '남산학사' not in print_course:
                    print_course.append('남산학사')
            elif token in ['그루터기', '그', 'r']:
                if '그루터기' not in print_course:
                    print_course.append('그루터기')
            elif token in ['전부출력', '모두출력', '전부', '모두']:
                full_print = True

    time_message = strftime('%m월 %d일(%a)', localtime())
    if is_lunch:
        message = ':sunny: ' + time_message + '중식 :sunny:\n'
    else:
        message = ':star2: ' + time_message + '석식 :star2:\n'

    html = urllib.urlopen(DGUCOOP_URL)
    soup = BeautifulSoup(html, 'lxml')
    courses = soup.find_all(True, {'bgcolor': '#FFFFFF'})

    for course_idx, course_val in enumerate(courses):
        if course_idx not in COURSE_INFO:
            continue
        if remove_noise(str(course_val)) == '휴무':
            for key in COURSE_INFO.keys():
                if key > course_idx:
                    cnt = COURSE_INFO[course_idx]['cnt']
                    COURSE_INFO[key - cnt] = COURSE_INFO[key]
                    del COURSE_INFO[key]
            continue
        courseInfo = COURSE_INFO[course_idx]
        course[courseInfo['name']] = []     # course['상록원']
        for idx, val in enumerate(courseInfo['details']):
            menu = []
            prefix = courseInfo['dinner_cnt'][idx]
            str_lunch = str(courses[course_idx + idx])
            str_dinner = str(courses[course_idx + idx + prefix])
            lunch = remove_noise(str_lunch)
            dinner = remove_noise(str_dinner)
            menu.append(val)        # 일품
            menu.append(lunch)      # 점심
            menu.append(dinner)     # 저녁
            course[courseInfo['name']].append(menu)
    for pc in print_course:
        message += '>*' + pc + '*\n'
        if pc in course:
            for p in course[pc]:
                if p[1 if is_lunch else 2]:
                    food = re.sub('\r\n', '\n', p[1 if is_lunch else 2])
                    food = ' || '.join(food.split('\n')) + '\n'
                    if p[1] == p[2]:
                        if full_print:
                            message += p[0] + ': ' + food
                    else:
                        message += p[0] + ': ' + food
    return channel, message
