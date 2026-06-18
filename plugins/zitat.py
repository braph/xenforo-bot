#!/usr/bin/env python3

import os
import subprocess

def _find_fortune_bin():
    candidates = [
        f'/usr/games/fortune',
        f'/usr/bin/fortune'
    ]

    for file in candidates:
        if os.path.exists(file):
            return file

def _find_fortune_file(topic):
    candidates = [
        f'/usr/share/games/fortunes/de/{topic}',
        f'/usr/share/fortunes/{topic}'
    ]

    for file in candidates:
        if os.path.exists(file):
            return file

def zitat(chatbot, args, message):
    fortune_bin = _find_fortune_bin()
    zitate_file = _find_fortune_file('zitate')
    r = subprocess.run([fortune_bin, zitate_file], stdout=subprocess.PIPE)
    r = r.stdout.decode('UTF-8')
    chatbot.send_message(r)
