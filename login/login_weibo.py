import requests
import json

from login.util import Util


class LoginHelper(object):
    def __init__(self):
        self.default_pwd = '抓包后输入其中的p'
        self.gsid = None
        pass

    def login(self, user='15800758995', pwd=None):
        if pwd:
            self.default_pwd = pwd
        body = {
            'p': self.default_pwd,
            's': '62f551c4',
            'u': user}
        r = requests.post('https://api.weibo.cn/2/account/login?c=iphone', data=body)
        try:
            self.gsid = r.json()['gsid']
        except:
            print('login error!!!')
            return

    pass


    def get_gsid(self):
        if not self.gsid:
            self.login()
        if not self.gsid:
            print('login error!!!')
            return
        return self.gsid
