# /usr/bin/python

# main file of al
# Louis
# 02/03/2017

import itchat
import requests
from settings import settings
from algorithms.fenke import fenke_api
import algorithms.utilities
import threading
import time


turing_bot_key = '05adb65eb0a94b5f9bb6a241f21e2f7c'


class Algorithms:
    def __init__(self):
        self.placeholder = 'placeholder: algo in algo_main.py'

        # get hospital list
        self.hospital_list = algorithms.utilities.get_hospital_list()

        # get hospital api
        self.hospital_api = {}
        for hospital in self.hospital_list:
            self.hospital_api[hospital] = algorithms.utilities.get_hospital_api(hospital)

        # get doctors list
        self.doctors_list = algorithms.utilities.get_doctor_list()

        # get list
        self.general_practitioners_list = algorithms.utilities.get_general_practitioner_list()

        self.suggestion_users = []
        self.suggestion_users_info = {}

        self.suggestion_message = ['',  # place holder
                                   '需要挂号请回复1\n' \
                                   '需要推荐全科医生请回复2',  # 1
                                   '检查完成后，上传病例或者告诉我你的药品、复诊时间，我将会提醒你定时吃药以及复诊',  # 2
                                   '挂号完成！',  # 3
                                   ]

    def hospital_suggestion_init(self, msg):
        user_alias = msg['User']['Alias']
        self.suggestion_users_info[user_alias] = msg
        self.suggestion_users_info[user_alias]['step'] = 1
        self.suggestion_users.append(user_alias)

    def hospital_suggestion(self, msg, status=None):
        """
        hospital_suggestion
        """

        user_alias = msg['User']['Alias']
        if user_alias not in self.suggestion_users:
            self.hospital_suggestion_init(msg)

        # 是否需要推荐医院
        if self.suggestion_users_info[user_alias]['step'] == 1:
            try:
                threading.Thread(target=send_message_delay,
                                 args=(self.suggestion_message[1], msg['User']['UserName'], 1.5),
                                 name=user_alias+'1').start()

                # send_message_delay(self.suggestion_message[1], msg['User']['UserName'], 5)
                self.suggestion_users_info[user_alias]['step'] = 2
            except Exception as e:
                if settings.debug:
                    print(e)

        # 挂号和推荐全科医生
        elif self.suggestion_users_info[user_alias]['step'] == 2:
            try:
                if status == '2-1':
                    doctors = '\n'.join(self.doctors_list)
                    send_message_delay(doctors, msg['User']['UserName'], 0)
                    threading.Thread(target=send_message_delay,
                                     args=(self.suggestion_message[2], msg['User']['UserName'], 3),
                                     name=user_alias+'1').start()

                    self.suggestion_users.remove(user_alias)
                    del (self.suggestion_users_info[user_alias])
                    # send_message_delay(self.suggestion_message[2], msg['User']['UserName'], 2)

                elif status == '2-2':
                    doctors = '\n'.join(self.general_practitioners_list)
                    send_message_delay(doctors, msg['User']['UserName'], 0)
                    threading.Thread(target=send_message_delay,
                                     args=(self.suggestion_message[2], msg['User']['UserName'], 3),
                                     name=user_alias + '1').start()

                    self.suggestion_users.remove(user_alias)
                    del (self.suggestion_users_info[user_alias])
                else:
                    self.suggestion_hospital_cancel(msg)

            except Exception as e:
                if settings.debug:
                    print(e)

    # def hospital_suggestion(self, msg):
    #     """
    #     hospital_suggestion
    #     """
    #
    #     user_alias = msg['User']['Alias']
    #     if user_alias not in self.suggestion_users:
    #         self.hospital_suggestion_init(msg)
    #
    #     # 是否需要推荐医院
    #     if self.suggestion_users_info[user_alias]['step'] == 1:
    #         try:
    #             threading.Thread(target=send_message_delay,
    #                              args=(self.suggestion_message[1], msg['User']['UserName'], 1.5),
    #                              name=user_alias+'1').start()
    #
    #             # send_message_delay(self.suggestion_message[1], msg['User']['UserName'], 5)
    #             self.suggestion_users_info[user_alias]['step'] = 2
    #         except Exception as e:
    #             if settings.debug:
    #                 print(e)
    #
    #     # 是否需要挂号
    #     elif self.suggestion_users_info[user_alias]['step'] == 2:
    #         try:
    #             hospitals_list = []
    #             for i in range(len(self.hospital_list)):
    #                 hospitals_list.append(str(i+1) + '. ' + self.hospital_list[i] + '\n')
    #             hospitals = ''.join(hospitals_list)
    #             send_message_delay(hospitals, msg['User']['UserName'], 0)
    #             threading.Thread(target=send_message_delay,
    #                              args=(self.suggestion_message[2], msg['User']['UserName'], 1),
    #                              name=user_alias+'1').start()
    #             # send_message_delay(self.suggestion_message[2], msg['User']['UserName'], 2)
    #
    #             self.suggestion_users_info[user_alias]['step'] = 3
    #         except Exception as e:
    #             if settings.debug:
    #                 print(e)
    #
    #     # 完成挂号
    #     elif self.suggestion_users_info[user_alias]['step'] == 3:
    #         try:
    #             # TODO: call real function to finish registration
    #             threading.Thread(target=send_message_delay,
    #                              args=(self.suggestion_message[3], msg['User']['UserName'], 1),
    #                              name=user_alias+'1').start()
    #             # send_message_delay(self.suggestion_message[3], msg['User']['UserName'], 2)
    #
    #             self.suggestion_users.remove(user_alias)
    #             del (self.suggestion_users_info[user_alias])
    #         except Exception as e:
    #             if settings.debug:
    #                 print(e)

    def suggestion_hospital_cancel(self, msg):
        user_alias = msg['User']['Alias']
        if user_alias in self.suggestion_users:
            self.suggestion_users.remove(user_alias)
        if user_alias in self.suggestion_users_info:
            del(self.suggestion_users_info[user_alias])
        send_message_delay('推荐取消！', msg['User']['UserName'], 1)


algo = Algorithms()


def send_message_delay(msg, user_name, delay_time):
    time.sleep(delay_time)
    itchat.send(msg, toUserName=user_name)


def get_response(msg):
    api_url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': turing_bot_key,
        'info': msg['Text'],
        'userid': 'louis',
    }
    try:
        if msg['Text'].startswith('?') or msg['Text'].startswith('？'):
            ret = fenke_api.fenke_api(msg['Text'][1:])
        elif msg['Text'].strip() == '帮助':
            ret = algorithms.utilities.help_message()
        else:
            return
            r = requests.post(api_url, data=data).json()
            # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
            ret = r.get('text')
        return ret

    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except Exception as e:
        if settings.debug:
            print(e)

        # 将会返回一个None
        return

# @itchat.msg_register(itchat.content.TEXT)
# def print_content(msg):
#     if settings.debug:
#         print(msg)
#
#     name = 'Not Found'
#
#     for friend in itchat.get_friends():
#         if friend['UserName'] == msg['FromUserName']:
#             name = friend['NickName']
#             break
#
#     return name + ', ' + msg['Text']


def suggestion_hospital(msg):
    user_alias = msg['User']['Alias']
    if msg['Text'].startswith('?') or msg['Text'].startswith('？'):
        algo.hospital_suggestion_init(msg)
        algo.hospital_suggestion(msg)
        return True
    elif msg['Text'] == '病历':
        send_message_delay('http://sample.zixuncr.com/sample.html', msg['User']['UserName'], 0)
        return False
    elif user_alias in algo.suggestion_users:
        if algo.suggestion_users_info[user_alias]['step'] == 2:
            if msg['Text'].strip() == '1':
                algo.hospital_suggestion(msg, status='2-1')
            elif msg['Text'].strip() == '2':
                algo.hospital_suggestion(msg, status='2-2')
            else:
                algo.suggestion_hospital_cancel(msg)
        # elif algo.suggestion_users_info[user_alias]['step'] == 3:
        #     try:
        #         hospital_id = int(msg['Text'])
        #         if 0 < hospital_id <= len(algo.hospital_list):
        #             algo.hospital_suggestion(msg)
        #         else:
        #             raise ValueError('Hospital ID error.')
        #
        #     except Exception as e:
        #         algo.suggestion_hospital_cancel(msg)
        #         if e is not ValueError and settings.debug:
        #             print(e)
        return True



@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    default_reply = 'I received: ' + msg['Text'] + '\nThis is only an auto-replay, when something wrong happens.'
    # 如果图灵Key出现问题，那么reply将会是None

    suggestion = suggestion_hospital(msg)
    if not suggestion:
        return

    ############
    # return  # Delete this line to re-connect to turing bot

    reply = get_response(msg)


    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    return reply or default_reply


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def group_reply(msg):
    reply = None
    if 'IsAt' in msg:
        if msg['IsAt']:
            reply = get_response(msg)
            default_reply = 'I received: ' + msg['Text'] + '\nThis is only an auto-replay, when something wrong happens.'
            return reply or default_reply
    else:
        return


# main
# only for test while developing
def main():
    pass


# call main
if __name__ == "main":
    main()
