# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
import json
import os
import sys
MESSAGE_CACHE_URL = './apps/message_cache/'


@on_command(['취소해!'])
def run(robot, channel, tokens, user, command):
    ''''''
    json_file = MESSAGE_CACHE_URL + user + channel + '.json'
    if os.path.isfile(json_file):
        result = json.loads(open(json_file).read())
        robot.client.api_call('chat.delete', ts=result['ts'], channel=result['channel'])
        os.remove(json_file)
    sys.exit()
    return channel, ''
