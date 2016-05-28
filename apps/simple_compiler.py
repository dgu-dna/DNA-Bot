from apps.decorators import on_command
from apps.slackutils import cat_token
from subprocess import check_output, CalledProcessError, STDOUT
import os
import re


@on_command(['!컴파일'])
def run(robot, channel, tokens, user, command):
    '''C, C++, Python 소스 실행시켜드림'''
    msg = ''
    if len(tokens) < 2:
        return channel, '자세한 사용방법은...'
    tokens[0] = tokens[0].strip()
    if tokens[0].lower() in ['c', 'c++']:
        source = cat_token(tokens, 1)
        source = re.sub('&amp;', '&', source)
        source = re.sub('&lt;', '<', source)
        source = re.sub('&gt;', '>', source)
        if tokens[0].lower() == 'c':
            open(user + '.c', 'w').write(source)
            msg += check_output(['gcc', user + '.c', '-o', user + '.out']).decode('utf-8')
            os.remove(user + '.c')
        else:
            open(user + '.cpp', 'w').write(source)
            try:
                msg += check_output(['g++', '-std=c++11' ,user + '.cpp', '-o', user + '.out'], stderr=STDOUT).decode('utf-8')
            except CalledProcessError as e:
                msg += e.output.decode('utf-8')
                return channel, msg
            os.remove(user + '.cpp')
        try:
            msg += check_output(['./' + user + '.out']).decode('utf-8')
        except CalledProcessError as e:
            msg += '> :warning: WARNING : Your program returned exit status `' + str(e.args[0]) +'`\n'
            msg += e.output.decode('utf-8')
        os.remove(user + '.out')
    if tokens[0].lower() in ['python', 'python3']:
        source = cat_token(tokens, 1)
        source = re.sub('&amp;', '&', source)
        source = re.sub('&lt;', '<', source)
        source = re.sub('&gt;', '>', source)
        open(user + '.py', 'w').write(source)
        try:
            if tokens[0].lower() == 'python':
                msg += check_output(['python',user + '.py'], stderr=STDOUT).decode('utf-8')
            else:
                msg += check_output(['python3',user + '.py'], stderr=STDOUT).decode('utf-8')
        except CalledProcessError as e:
            msg += e.output.decode('utf-8')
            return channel, msg
        os.remove(user + '.py')
    return channel, msg

