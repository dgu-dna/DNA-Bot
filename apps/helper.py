# coding: utf-8
from __future__ import unicode_literals
from decorators import on_command


@on_command(['!생협', 'dgucoop', '!ㅅㅎ','!tg'])
def run(robot, channel, tokens, user):
    '''도움말을 출력해드려요'''
    return channel, '\n'.join(robot.docs)
