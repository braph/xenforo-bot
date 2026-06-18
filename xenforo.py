import re
import json
import time
import requests
from lxml import html

def print_html(src):
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(src, "html.parser")
    print(soup.prettify())

class XenForoURLs:
    def __init__(self, main_url):
        self.first_url       = f'{main_url}/psychose/'
        self.login_url       = f'{main_url}/psychose/login/login'
        self.chat_update_url = f'{main_url}/psychose/index.php?chat/update'
        self.chat_submit_url = f'{main_url}/psychose/index.php?chat/submit'

class XenForoConfig:
    def __init__(self):
        self.urls           = None
        self.email          = None
        self.password       = None
        self.error_log_file = None
        self.debug_log_file = None

    @staticmethod
    def from_file(file):
        cfg = XenForoConfig()

        with open(file, 'r') as fh:
            data = json.load(fh)

        cfg.urls           = XenForoURLs(data['main_url'])
        cfg.email          = data['email']
        cfg.password       = data['password']
        cfg.error_log_file = data['error_log_file']
        cfg.debug_log_file = data['debug_log_file']
        
        return cfg

class XenForoClient:
    def __init__(self, config):
        self.config = config
        self.session = requests.Session()
        self.xf_token = None

    @staticmethod
    def _extract_xftoken(src):
        m = re.search(r'name="_xfToken"\s+value="([^"]+)"', src)
        if not m:
            raise Exception('No _xfToken found')

        return m.group(1)

    def login(self):
        r = self.session.get(self.config.urls.first_url)
        self.xf_token = self._extract_xftoken(r.text)

        r = self.session.post(self.config.urls.login_url, {
            '_xfToken': self.xf_token,
            'login': self.config.email,
            'password': self.config.password,
            'remember': 1
        })
        self.xf_token = self._extract_xftoken(r.text)

    def send_message(self, message_html):
        data = {
            "users": { "1": [ 2498, 2180, "1968", "2762", "2299", "1441" ] },
            "channel": "room",
            "room_id": "1",
            "last_id": { "1": 94762 },
            "conv_id": 0,
            "conv_items": "",
            "conv_unread": [],
            "conv_last_id": 0,
            "message_html": message_html,
            "_xfResponseType": "json",
            "_xfWithData": 1,
            "_xfRequestUri": "/psychose/chat/",
            "_xfToken": self.xf_token
        }

        self.session.post(self.config.urls.chat_submit_url, data)

    def get_messages(self, last_id):
        t = int(time.time())

        data = {
            #"users": {"1": [1441,2498,2180,2299]},
            "channel":"room",
            "room_id":"1",
            "last_id": {"1":last_id},
            "conv_id":0,
            "conv_unread":[],
            "conv_only":0,
            "conv_items":"",
            "conv_last_active":t,
            "conv_last_update":t,
            "user_last_update":t,
            "is_chat_page":1,
            "hide_tabs":0,
            "_xfResponseType":"json",
            "_xfWithData":1,
            "_xfRequestUri":"/psychose/chat/",
            "_xfToken": self.xf_token
        }

        r = self.session.post(self.config.urls.chat_update_url, data)
        js = r.json()
        messages = js['rooms']['1']['messages']
        return self.parse_message_result(messages)

    def parse_message_result(self, messages_html):
        #print_html(messages_html)

        res = []
        doc = html.fromstring(messages_html)

        for li in doc.cssselect('.siropuChatMessageRow'):
            left = li.cssselect('.siropuChatMessageContentLeft')
            user = li.cssselect('.username')[0].text
            text = li.cssselect('.siropuChatMessageText')[0].text_content()
            data_id = int(li.attrib['data-id'])

            res.append({
                'user': user,
                'text': text,
                'message_id': data_id
            })

        return res

    def like_post(self, post_id, reaction_id=1):
        self.session.post(f'{self.config.main_url}/psychose/posts/{post_id}/react', {
            '_xfToken': self.xf_token,
            'reaction_id': reaction_id
        })
