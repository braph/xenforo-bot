#!/usr/bin/python3

import time
import traceback

class XenForoChatBot:
    def __init__(self, client):
        self.client = client
        self.last_id = 0
        self.received_message_ids = set()
        self.commands = {}

    def _run(self):
        self.client.login()
        self.loop_init()

        while True:
            self.loop()
            time.sleep(1)

    def run(self):
        while True:
            try:
                self._run()
            except Exception as e:
                with open(self.client.config.error_log_file, 'a') as fh:
                    traceback.print_exc(file=fh)
                    time.sleep(1)

    def loop_init(self):
        messages = self.client.get_messages(self.last_id)
        for message in messages:
            message_id = message['message_id']
            self.last_id = max(message_id, self.last_id)
            self.received_message_ids.add(message_id)

    def loop(self):
        messages = self.client.get_messages(self.last_id)
        for message in messages:
            message_id = message['message_id']
            self.last_id = max(message_id, self.last_id)

            if message_id not in self.received_message_ids:
                try:
                    self.handle_message(message)
                finally:
                    self.received_message_ids.add(message_id)

    def handle_message(self, message):
        text       = message['text']
        message_id = message['message_id']
        user       = message['user']
        print('>>>', message_id, user, text)

        text = text.strip()

        if not text:
            return

        if text[0] == '!':
            text = text[1:]
            splitted = text.split(maxsplit=1)
            command = splitted[0].lower()

            try:
                args = splitted[1]
            except:
                args = ''

            if command in self.commands:
                self.commands[command](self, args, message)

    def send_message(self, message):
        self.client.send_message(message)

    def register_command(self, command, callback):
        self.commands[command] = callback
