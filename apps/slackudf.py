import imp
settings = imp.load_source('settings','./settings.py')
BOT_NAME = settings.BOT_NAME
ICON_URL = settings.ICON_URL
#from settings import BOT_NAME, ICON_URL

def send_msg(robot, channel, message):
	robot.client.api_call('chat.postMessage',username=BOT_NAME, as_user='false',icon_url=ICON_URL,channel=channel,text=message)

def cat_token(tokens, prefix):
    fulltok=''
    if(len(tokens) <= prefix):
        return ''
    itertok=iter(tokens)
    for i in range(prefix):
        next(itertok)
    for token in itertok:
        fulltok += token + ' '
    return fulltok[:-1]
