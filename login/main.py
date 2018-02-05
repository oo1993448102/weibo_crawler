import execjs

from login.db_helper import DatabaseHelper
from login.helper import Helper
from login.util import Util

if __name__ == '__main__':
    helper = Helper()
    # helper.get_friends_timeline(max_count=5)
    helper.get_someone_info('') #输入contailerId
    pass
