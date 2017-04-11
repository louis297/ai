#!/usr/bin/python

# core algorithms interface
# provide interface between main controller and algorithms part
# Louis
# 04/07/2017

def help():
    ret = '''#   查询分科信息
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
