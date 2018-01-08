import pymongo

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
                timeline_collection.insert({'id': str(status['id']), 'status': status})
        pass

    # 清除新鲜事
    def clearTimeline(self):
        global timeline_collection
        if not timeline_collection:
            timeline_collection = self.database['timeline']
        timeline_collection.drop()
        pass
