import requests

from login.db_helper import DatabaseHelper
from login.login_weibo import LoginHelper

database_helper = None


class Helper(object):
    def __init__(self):
        self.max_count = 1
        global database_helper
        database_helper = DatabaseHelper()
        pass

    # 新鲜事api
    def get_friends_timeline(self, max_count=None, count=5, **bodys):
        if max_count:
            self.max_count = max_count
        gsid = LoginHelper().get_gsid()
        if gsid:
            params = {'gsid': gsid,
                      'c': 'iphone',
                      's': 'd76eb238',
                      }
            body = {
                'count': count,
            }
            body = dict(body, **bodys)
            r = requests.post('https://api.weibo.cn/2/statuses/friends_timeline', params=params, data=body)
            print(r.url)
            global database_helper
            database_helper.saveTimeline(r.json()['statuses'])
            self.max_count -= 1
            if self.max_count > 0:
                self.get_friends_timeline(max_id=r.json()['max_id'])
        pass

    # 拉取特定的某个人的信息
    def get_someone_info(self, containerid, count=20, page=1):
        gsid = LoginHelper().get_gsid()
        if gsid:
            params = {
                'gsid': gsid,
                'c': 'iphone',
                's': 'd76eb238',
                'count': count,
                'containerid': containerid,
                'from': '1081093010',
                'page': page
            }
            r = requests.get('https://api.weibo.cn/2/cardlist', params=params)
            print(r.url)
            if len(r.json()['cards']) == 0:
                return
            global database_helper
            if database_helper.saveSomeone(containerid, r.json()['cards']):
                self.get_someone_info(containerid, page=page + 1)
            else:
                return

        pass
