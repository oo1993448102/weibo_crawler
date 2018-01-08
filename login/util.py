import json


class Util(object):

    # json格式化
    @staticmethod
    def format(str):
        return json.dumps(str.json(), indent=4, ensure_ascii=False)
