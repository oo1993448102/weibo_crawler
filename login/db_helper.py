import pymongo

from login.util import Util

timeline_collection = None


class DatabaseHelper(object):
    def __init__(self):
        client = pymongo.MongoClient('localhost', 27017)
        self.database = client['weibo']

    # 将新鲜事保存到mongo中
    def saveTimeline(self, timeline_list):
        global timeline_collection
        if not timeline_collection:
            timeline_collection = self.database['timeline']
        for status in timeline_list:
            # 查询是否已在表内
            if timeline_collection.find({'id': str(status['id'])}).count() == 0:
                # print(str(status['id']))
                timeline_collection.insert({'id': str(status['id']), 'status': status})
        pass

    # 清除新鲜事
    def clearTimeline(self):
        global timeline_collection
        if not timeline_collection:
            timeline_collection = self.database['timeline']
        timeline_collection.drop()
        pass

    # 保存某人事件
    def saveSomeone(self, containerId, card_list):
        needNext = True
        him_collection = self.database['someone']
        # him_collection.drop()
        others = []
        cards = []
        for item in card_list:
            # 区分是否为本人微博
            if item.get('card_group'):
                others.append(item)
            else:
                cards.append(item)
        cards.sort(key=lambda k: k['mblog']['id'], reverse=True)
        if him_collection.find({'id': containerId}).count() == 0:
            him_collection.insert({'id': containerId, 'timeline': cards, 'other': others})
            return True
        else:
            cursor = him_collection.find({'id': containerId})
            for item in cursor:
                timeline_list_temp = []
                other_list_temp = []
                if item.get('timeline'):
                    lines = item['timeline']
                else:
                    lines = []
                for card in cards:
                    if card in lines:
                        print('same')
                        print(card)
                        needNext = False
                        break
                    else:
                        timeline_list_temp.append(card)
                        # lines.append(card)
                        try:
                            Util.send_mail(card['mblog']['text'])
                        except:
                            Util.send_mail("他发布了新动态")
                lines = timeline_list_temp + lines
                if item.get('other'):
                    other = item['other']
                else:
                    other = []
                for oth in others:
                    if oth in other:
                        needNext = False
                        print('same')
                        print(oth)
                        break
                    else:
                        other_list_temp.append(oth)
                        Util.send_mail("他点赞了别人的微博")
                other = other_list_temp + other
                lines.sort(key=lambda k: k['mblog']['id'], reverse=True)
                him_collection.update_one(
                    {'id': containerId},
                    {"$set": {"timeline": lines, "other": other}},
                )
            return needNext

    pass
