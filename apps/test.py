# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.decorators import on_command
from apps.slackutils import send_msg
import time
import json

@on_command(['테스팅'])
def run(robot, channel, tokens, user, command):
    '''디버깅용 기능입니다'''
    attach_json = {
            "type": "message",
            "attachments": [
                            {
                                "fallback": "Required plain-text summary of the attachment.",
                                "color": "#FF0000",
                                "pretext": "Optional text that appears above the attachment block",
                                "author_name": "작성자",
                                "author_link": "http://www.naver.com/",
                                "author_icon": "http://feonfun.com/slack_api_logo_16.jpg",
                                "title": "제목!",
                                "title_link": "https://api.slack.com/",
                                "text": "설명!",
                                #"fields": [
                                #    {
                                #        "title": "필드 제목!",
                                #        "value": "필드 설명?",
                                #        "short": "false"
                                #                                                                                                                        }
                                #    ],
                                "thumb_url": "http://feonfun.com/slack.jpg"
                                }
                            ],
            "channel": channel
                    }
    att = [
                            {
                                "fallback": "Required plain-text summary of the attachment.",
                                "color": "#FF0000",
                                "pretext": "Optional text that appears above the attachment block",
                                "author_name": "작성자",
                                "author_link": "http://www.naver.com/",
                                "author_icon": "http://feonfun.com/slack_api_logo_16.jpg",
                                "title": "제목!",
                                "title_link": "https://api.slack.com/",
                                "text": "설명!",
                                #"fields": [
                                #    {
                                #        "title": "필드 제목!",
                                #        "value": "필드 설명?",
                                #        "short": "false"
                                #                                                                                                                        }
                                #    ],
                                "thumb_url": "http://feonfun.com/slack.jpg"
                                }
                            ]
    #presence_json = {"type": "presence_change", "user": "U0SP3F8K0", "presence": "away"}
    #typing_json = {"type": "user_typing", "user": user, "channel": channel}
    #message_json = {"type": "message", "channel": channel, "text": '에에에엥?'}
    #robot.client.server.send_to_websocket(message_json)
    #result = robot.client.api_call('chat.postMessage',username='Cheer Up!',channel=channel,attachments=json.dumps(att))
    msg = '주작'
    result = robot.client.api_call('chat.postMessage',username='Cheer Up!',channel=channel,text='주작')
    #msg = '바보!'
    #result = send_msg(robot, channel, msg)
    #time.sleep(5)
    #result = robot.client.api_call('chat.delete', ts=result['ts'], channel=channel)
    #while True:
    #    msg += '작'
    #    result = robot.client.api_call('chat.update', ts=result['ts'], channel=channel, text=msg)
    #    time.sleep(1)
    result = robot.client.api_call('im.open', user=user)
    result = send_msg(robot, result['channel']['id'], 'I love you')
    #result = robot.client.api_call('files.upload', file=@README.md, filename='README.md', title='봇 설명!', initial_comment = '캬!', channels=channel)
    print(result)
    #result =robot.client.server.send_to_websocket(json.dumps(attach_json))
    #print(result)
    msg = ' '
    msg += str(user)
    return channel, msg
#{
#    "type": "presence_change", 
#    "user": "U0SPF91EE", 
#    "presence": "away"
#}
#{
#    "type": "user_typing", 
#    "user": "U0SPF91EE", 
#    "channel": "C0ZGFDY9K"
#}

# Bot Message
#{
#    "text": "\uc5d0\uc5d0\uc5d0\uc5e5?", 
#    "ts": "1463831471.019152", 
#    "user": "U0SP3F8K0", 
#    "team": "T0SMCFPNF", 
#    "type": "message", 
#    "channel": "C0ZGFDY9K"
#}

#
#{
#    "event_ts": "1463624837.335053", 
#    "ts": "1463624837.017871", 
#    "subtype": "message_changed", 
#    "message": {
#        "text": "\u3137\u3137\u3137\u314babcd", 
#        "type": "message", 
#        "user": "U0SPF91EE", 
#        "ts": "1463624404.017861", 
#        "edited": {
#            "user": "U0SPF91EE", 
#            "ts": "1463624837.000000"
#        }
#    }, 
#    "type": "message", 
#    "hidden": true, 
#    "channel": "C0ZGFDY9K", 
#    "previous_message": {
#        "text": "\u3137\u3137\u3137\u314b", 
#        "type": "message", 
#        "user": "U0SPF91EE", 
#        "ts": "1463624404.017861", 
#        "edited": {
#            "user": "U0SPF91EE", 
#            "ts": "1463624738.000000"
#        }
#    }
#}
