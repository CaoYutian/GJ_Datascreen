#Author:Sunshine丶天
# -*- coding: utf-8 -*-
# 车辆按时间排序
import os
import threading
import multiprocessing

def ConfiationAlgorithm(str):
    if len(str) <= 1: #子序列
        return str
    mid = (len(str) // 2)
    left = ConfiationAlgorithm(str[:mid])#递归的切片操作
    right = ConfiationAlgorithm(str[mid:len(str)])
    result = []

    while len(left) > 0 and len(right) > 0:
        if (left[0] <= right[0]):
            #result.append(left[0])
            result.append(left.pop(0))
            #i+= 1
        else:
            #result.append(right[0])
            result.append(right.pop(0))
            #j+= 1

    if (len(left) > 0):
        result.extend(ConfiationAlgorithm(left))
    else:
        result.extend(ConfiationAlgorithm(right))
    return result

def analyze(filepath,basePath,str_name):
    data = []
    sourceArr = []
    with open(filepath, "r", encoding='utf-8') as f_out:
        for line in f_out:
            line = line.strip()
            values = line.split(',')
            data.append(values[1])
            sourceArr.append(values)
        Arr = ConfiationAlgorithm(sourceArr)

        fp = basePath + str_name + Arr[0][0] + '.txt'
        for re in Arr:
            f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
            valueLine = re[0] + ',' + re[1] + ',' + re[2] + ',' + re[3] + '\n'
            f_in.write(valueLine)
            f_in.close()

def run_yc(basePath,count,allCount):
    rootdir = basePath + '有效车辆归类'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件

    start_index = int(len(list) * count / allCount)
    end_index = int(len(list) * (count + 1) / allCount)

    for i in range(start_index, end_index):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if str(path).endswith('txt'):
                try:
                    analyze(path,basePath,'排序后车辆/')
                except:
                    fp = basePath + '错误/排序错误文件.txt'
                    f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
                    f_in.write(list[i] + '\n')
                    f_in.close()

def run_all(basePath,count,allCount):
    rootdir = basePath + '完整有效车辆归类'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    start_index = int(len(list) * count / allCount)
    end_index = int(len(list) * (count + 1) / allCount)

    for i in range(start_index, end_index):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if str(path).endswith('txt'):
                # analyze(path, basePath, '完整排序后车辆/')
                try:
                    analyze(path, basePath,'完整排序后车辆/')
                except:
                    fp = basePath + '错误/完整排序错误文件.txt'
                    f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
                    f_in.write(list[i] + '\n')
                    f_in.close()

def run_sortTime(basePath,type,threadCount):
    if type == 'yc':
        pool = multiprocessing.Pool(processes=threadCount)
        for i in range(threadCount):
            pool.apply_async(run_yc, (basePath, i, threadCount))
        pool.close()
        pool.join()
        # thread_arr = []
        # for i in range(threadCount):
        #     t = threading.Thread(target=run_yc, args=(basePath,i,threadCount))
        #     t.start()
        #     thread_arr.append(t)
        #
        # # join() 方法是等待线程执行完毕
        # for thread in thread_arr:  # 等待所有线程执行完毕
        #     thread.join()

    elif type == 'all':
        pool = multiprocessing.Pool(processes=threadCount)
        for i in range(threadCount):
            pool.apply_async(run_all, (basePath, i, threadCount))
        pool.close()
        pool.join()
        # thread_arr = []
        # for i in range(threadCount):
        #     t = threading.Thread(target=run_all, args=(basePath, i, threadCount))
        #     t.start()
        #     thread_arr.append(t)
        #
        # # join() 方法是等待线程执行完毕
        # for thread in thread_arr:  # 等待所有线程执行完毕
        #     thread.join()