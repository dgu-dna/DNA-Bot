# coding: utf-8
from __future__ import unicode_literals
import os
import sys
import gevent
import logging
from gevent.pool import Pool
from gevent.monkey import patch_all
from importlib import import_module
from slackclient import SlackClient
from settings import BOT_NAME, ICON_URL, SLACK_TOKEN_MGR
patch_all()
from subprocess import check_output

pool = Pool(20)

CMD_PREFIX = ''
logger = logging.getLogger()

class Robot(object):
    def __init__(self):
        self.client = SlackClient(SLACK_TOKEN_MGR)
        self.apps, self.docs = self.load_apps()

    def load_apps(self):
        docs = ['']
        apps = {}

        app = import_module('apps.system')
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
        tokens = text.split(' ', 1)
        if 1 < len(tokens):
            return tokens[0], tokens[1]
        else:
            return (text, '')

    def run(self):
        if self.client.rtm_connect():
            debug_chn = '#bot'
            if os.path.isfile('booting_mgr'):
                file = open('booting_mgr','r')
                reboot_chn = file.readline()
		self.client.api_call('chat.postMessage',username=BOT_NAME+' 매니저', as_user='false',icon_url=ICON_URL,channel=reboot_chn,text='재시작 완료')
                os.remove('booting_mgr')
            log_file = check_output(['ls', '-c', './log']).split('\n')[0]
            log_file = open('./log/'+log_file,'r')
            is_debug = False
            while True:
                if os.path.isfile('DEBUG'):
                    log_file.close()
                    log_file = check_output(['ls', '-c', './log']).split('\n')[0]
                    log_file = open('./log/'+log_file,'r')
                    dbg_file = open('DEBUG','r')
                    dbg_chn = dbg_file.readline()
                    dbg_file.close()
                    is_debug = True
                    os.remove('DEBUG')
                elif os.path.isfile('DEBUG_'):
                    os.remove('DEBUG_')
                    is_debug = False
                if is_debug:
                    txt = ''
                    txt = line = log_file.readline()
                    while line:
                        line = log_file.readline()
                        txt += line
                    if txt:
                        self.client.api_call('chat.postMessage',username=BOT_NAME+' 매니저(Debug)', as_user='false',icon_url=ICON_URL,channel=dbg_chn,text=txt)
                events = self.client.rtm_read()
                if events:
                    messages = self.extract_messages(events)
                    self.handle_messages(messages)
                gevent.sleep(1.5)


if '__main__' == __name__:
    robot = Robot()
    robot.run()
