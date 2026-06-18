#!/usr/bin/env python3

import subprocess

_PROVIDER   = 'sky'
_PRE_PROMPT = 'Du bist ein ChatBot. Antworte in nicht mehr als 100 Woertern'

def ki(chatbot, args, message):
    cmd = ['tgpt', '--provider', _PROVIDER, '--preprompt', _PRE_PROMPT, '--whole', '--quiet', args]
    r = subprocess.run(cmd, stdout=subprocess.PIPE)
    r = r.stdout.decode('UTF-8')
    chatbot.send_message(r)
