# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import cat_token

@on_command(['!말해'])
def run(robot, channel, tokens, user, command):
    '''시킨대로 말함'''
    if len(tokens) > 1:
        if tokens[0][1] == '#':
            msg = ' '.join(tokens).split(' ', 1)[1]
            #msg = cat_token(tokens,1)
            return tokens[0][2:-1], msg
    msg = ' '.join(tokens)
    #msg = cat_token(tokens,0)
    return channel, msg
