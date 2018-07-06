#Author:Sunshine丶天
import os
import sys
import time
from core import clean_datasource
from core import classify_car
from core import sort_time
from core import calc_parkTime
from core import getcarlist
from core import synthetic

def run(basePath):
    # 创建文件
    # print('\n 1')
    # clean_datasource.mkdir(basePath)
    # time.sleep(3)
    #
    # # 查找液厂周边2KM内经过的车辆
    # print('\n 2')
    # clean_datasource.clean_start(basePath)
    # time.sleep(14400)

    # 液厂周边车辆归类
    print('\n 3')
    classify_car.run_yc(basePath)
    time.sleep(2)

    # 液厂周边车辆按时间排序
    print('\n 4')
    sort_time.run_sortTime(basePath,'yc',30)
    time.sleep(2)

    # 计算液厂周边车辆停车点
    '''
        basePath: 路径
        'yc'：选择跑液厂周围 还是全部数据
        8：多进程的数量
    '''
    print('\n 5')
    calc_parkTime.run_parkTime(basePath,'yc',30)
    time.sleep(2)

    # 获取有效的车辆名单
    print('\n 6')
    getcarlist.getcarlist(basePath)
    time.sleep(2)

    #全数据有效车辆归类
    print('\n 7')
    classify_car.run_all(basePath)
    time.sleep(2)

    # 全数据车辆按时间排序
    print('\n 8')
    sort_time.run_sortTime(basePath,'all',30)
    time.sleep(2)

    # 全数据车辆停车点
    print('\n 9')
    '''
        basePath: 路径
        'all'：选择跑液厂周围 还是全部数据
        8：多线程的数量
        '''
    calc_parkTime.run_parkTime(basePath,'all',30)
    time.sleep(2)

    synthetic.run_synthetic(basePath)
