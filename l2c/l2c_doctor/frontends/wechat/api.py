# /usr/bin/python

# frontend - wechat
# frontend interface to wechat
# Louis
# 02/11/2017

import itchat


class Frontend:

    friends_info = {}
    groups_info = {}

    # input message
    def chat_in(self, str_in):
        return str_in

    # output message
    def chat_out(self, str_out):
        return str_out

    # wechat login
    def login(self):
        itchat.auto_login(hotReload=True, enableCmdQR=2)

    def get_friends(self):
        self.friends_info = itchat.get_friends()

    def get_groups(self):
        self.groups_info = itchat.get_contact()





frontend = Frontend()
