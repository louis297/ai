#!/usr/bin/python

# core algorithms interface
# provide interface between main controller and algorithms part
# Louis
# 04/07/2017


def help_message():
    ret = '''?   查询分科信息
帮助   查看帮助信息
其他   AI闲聊模式
          '''
    return ret


# TODO: get real hospital list
def get_hospital_list():
    return ['测试医院1', '测试医院2']


# TODO: get real hospital api
def get_hospital_api(hospital):
    return hospital + ' fake_api'

#TODO: get real doctors:
def get_doctor_list():
    return ['推荐医生1：挂号链接1', '推荐医生2：挂号链接2']


# TODO: get real general practitioner list
def get_general_practitioner_list():
    return ['全科医生1', '全科医生2']
