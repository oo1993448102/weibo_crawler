import execjs

from login.helper import Helper

if __name__ == '__main__':
    helper = Helper()
    # DatabaseHelper().clearTimeline()
    helper.get_friends_timeline(max_count=5)
    pass
