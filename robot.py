# coding: utf-8
from __future__ import unicode_literals
import os
import sys
import gevent
import logging
from gevent.pool import Pool
from gevent.monkey import patch_all
from redis import StrictRedis
from importlib import import_module
from slackclient import SlackClient
from settings import APPS, BOT_NAME, ICON_URL, SLACK_TOKEN, REDIS_URL
patch_all()

pool = Pool(20)

CMD_PREFIX = ''
logger = logging.getLogger()


class RedisBrain(object):
    def __init__(self):
        try:
            self.redis = StrictRedis(host=REDIS_URL)
        except Exception as e:
            logger.error(e)
            self.redis = None

    def set(self, key, value):
        if self.redis:
            self.redis.set(key, value)
            return True
        else:
            return False

    def get(self, key):
        if self.redis:
            return self.redis.get(key)
        return None


class Robot(object):
    def __init__(self):
        self.client = SlackClient(SLACK_TOKEN)
#        self.brain = RedisBrain()
        self.apps, self.docs = self.load_apps()

    def load_apps(self):
        docs = ['승규가 할 수 있는 것들이에요! >_<(새 기능 건의 환영)', '='*40]
        apps = {}

        for name in APPS:
            app = import_module('apps.%s' % name)
            if name != 'system':
                docs.append(
                  '   `%s` : %s' % ('`, `'.join(app.run.commands), app.run.__doc__)
                )
            for command in app.run.commands:
                apps[command] = app

        return apps, docs

    def handle_messages(self, messages):
        for channel, text, user in messages:
            command, payloads = self.extract_command(text)
            if not command:
                continue

            app = self.apps.get(command, None)
            if not app:
                continue
            arguments = (self, channel, payloads, user)
            pool.apply_async(func=app.run, args=arguments)

    def extract_messages(self, events):
        messages = []
        for e in events:
            user = e.get('user', '')
            channel = e.get('channel', '')
            text = e.get('text', '')
            if channel and text:
                messages.append((channel, text, user))
        return messages

    def extract_command(self, text):
        # if CMD_PREFIX != text[0]:
        #    return (None, None)
        tokens = text.split(' ', 1)
        if 1 < len(tokens):
            return tokens[0], tokens[1]
        else:
            return (text, '')

    def run(self):
        if self.client.rtm_connect():
            debug_chn = '#bot'
            if os.path.isfile('booting'):
                file = open('booting','r')
                debug_chn = file.readline()
                #self.client.rtm_send_message(reboot_chn,'rebooted successfully')
		self.client.api_call('chat.postMessage',username=BOT_NAME, as_user='false',icon_url=ICON_URL,channel=debug_chn,text='나 왔음')
                os.remove('booting')
            while True:
                events = self.client.rtm_read()
                if events:
                    messages = self.extract_messages(events)
                    self.handle_messages(messages)
                gevent.sleep(0.3)


if '__main__' == __name__:
    robot = Robot()
    robot.run()
