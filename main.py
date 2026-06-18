#!/usr/bin/env python3

import argparse

from xenforo import XenForoClient, XenForoConfig
from chatbot import XenForoChatBot

from plugins.ki     import ki
from plugins.zitat  import zitat
from plugins.choose import choose

argp = argparse.ArgumentParser()
argp.add_argument('-c', '--config', required=True)
opts = argp.parse_args()

config  = XenForoConfig.from_file(opts.config)
client  = XenForoClient(config)
chatbot = XenForoChatBot(client)

chatbot.register_command('ki',      ki)
chatbot.register_command('zitat',   zitat)
chatbot.register_command('choose',  choose)

chatbot.run()
