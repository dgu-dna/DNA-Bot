from importlib import import_module
import json
import re

USER = 'U01234567'
CHANNEL = 'C01234567'


class Client(object):
    def api_call(self, type, username, as_user='false', icon_url=None, channel=None, attachments=None, text=None):
        if not (text or attachments):
            print('api_call error() : you must give text or attachments')
            return
        if text:
            print(username + ' : ' + text)
        else:
            print(username + ' : ' + attachments)


class unitRobot(object):
    def __init__(self):
        self.client = Client()


def extract_command(text):
    tokens = text.split(' ', 1)
    if 1 < len(tokens):
        return tokens[0], tokens[1]
    else:
        return (text, '')


if __name__ == '__main__':
    robot = unitRobot()
    print('App\'s filename(without .py) >> ', end='')
    module_name = input()
    module = import_module('apps.%s' % module_name)
    print('APP\'s COMMANDS :' + '`, `'.join(module.run.commands))
    print('APP\'s DOC :' + module.run.__doc__)
    input_str = ''
    while input_str != 'exit':
        print('The input message : ', end='')
        input_str = input()
        command, payloads = extract_command(input_str)
        if not command:
            continue
        if command in module.run.commands:
            module.run(robot, CHANNEL, payloads, USER, command)
