# /usr/bin/python

# frontend
# frontend interface main controller
# Louis
# 02/11/2017

# comment some of the apis will improve the speed
from frontends.wechat.api import *

from settings import settings

frontend.login()
frontend.get_friends()
frontend.get_groups()

if settings.debug:
    print('-'*10 + 'Friends' +'-'*10)
    for friend in frontend.friends_info:
        print(friend['NickName'], friend['UserName'])
    print('-'*27)
