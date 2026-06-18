#!/usr/bin/env python3

import shlex
import random

_ANSWERS = {
    'Ja':                   10,
    'Nein':                 10,
    'Du spinnst!':          1,
    'Vielleicht':           1,
}

def _choose(args):
    args = shlex.split(args)

    if len(args) <= 1:
        return random.choices(list(_ANSWERS.keys()), weights=list(_ANSWERS.values()), k=1)[0]
    else:
        return random.choice(args)

def choose(chatbot, args, message):
    choice = _choose(args)
    chatbot.send_message(f'{message['user']}: {choice}')
