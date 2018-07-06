#Author:Sunshine丶天
import os
import time

def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    # path = path.rstrip("/")
    dir_arr = ['YuanShiData','有效车辆归类','排序后车辆','停车点','完整有效车辆归类','完整排序后车辆','完整停车点','错误']
    for dir in dir_arr:
        path_new = path + dir
        # 判断路径是否存在
        isExists = os.path.exists(path_new)

        # 判断结果
        if not isExists:
            # 如果不存在则创建目录
            # 创建目录操作函数
            os.makedirs(path_new)
        else:
            # 如果目录存在则不创建，并提示目录已存在
            pass

def clean_start(basePath):
    basePath2 = basePath.rstrip("/")
    basePath2 = basePath2.replace("Data_", "20");
    # 编译c++代码
    os.system('g++ /data/030/ailng/GJ_Datascreen/bin/clean.cpp -o /data/030/ailng/clean')
    time.sleep(1)

    os.system('cd /data/030/ailng')
    print(os.system('pwd'))
    for i in range(1,32):
        va = str(i)
        if len(va) == 1:
            va = '0' + str(i)
        else:
            va = va

        inPutPath = '"%s%s/"' % (basePath2, va)
        outPutPaht = '"%s%s/"' % (basePath, 'YuanShiData')
        command_cppClean = ('nohup ./clean %s %s &')%(inPutPath,outPutPaht)
        os.system(command_cppClean)
        time.sleep(1)
    print('c++ 已运行')
