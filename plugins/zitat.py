#!/usr/bin/env python3

import subprocess

def zitat(chatbot, args, message):
    r = subprocess.run(['fortune', 'zitate'], stdout=subprocess.PIPE)
    r = r.stdout.decode('UTF-8')
    chatbot.send_message(r)
