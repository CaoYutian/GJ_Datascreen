# -*- coding: utf-8 -*-
#Author:Sunshine丶天
# 车辆归类
import os
import multiprocessing

def analyze(filepath,basePath,keyDic):
    with open(filepath, "r", encoding='utf-8') as f_out:
        for line in f_out:
            line = line.strip()
            values = (line.split(','))  # 通过'，'切割
            key = values[0]+'_'+values[1]

            fp = basePath + '完整有效车辆归类/%s.txt' % key
            if key in keyDic:
                f_in = open(fp, "a+",encoding='utf-8',errors='ignore')
                valueLine = key + ',' + values[7] + ',' + values[9] + ',' + values[10] + '\n'
                f_in.write(valueLine)
                f_in.close()

def run_all_subP(basePath,va):
    keyDic = {}
    with open(basePath + 'carlist.txt', "r", encoding='utf-8') as f_out:
        keyArr = []
        for line in f_out:
            line = line.strip()
            keyArr.append(line)

            # 合成字典 key值查询快
            keyDic = dict(zip(keyArr, range(len(keyArr))))

    basePath2 = basePath
    basePath = basePath.replace("Data_", "20");
    basePath = basePath.rstrip("/")
    rootdir = '%s%s' % (basePath, va)
    print('完整归类--->',rootdir)
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if str(path).endswith('txt'):
                try:
                    analyze(path, basePath2, keyDic)
                except:
                    fp = basePath + '错误/完整归类错误文件.txt'
                    f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
                    f_in.write(list[i] + '\n')
                    f_in.close()

# 多进程并发
def run_all(basePath):
    pool = multiprocessing.Pool(processes=31)
    for i in range(1,32):
        va = str(i)
        if len(va) == 1:
            va = '0' + str(i)
        else:
            va = va
        pool.apply_async(run_all_subP,(basePath,va))
    pool.close()
    pool.join()

# ============================ 分割线 ============================
def analyze_yc(filepath,basePath):
    with open(filepath, "r", encoding='utf-8') as f_out:
        for line in f_out:
            try:
                line = line.strip()
                values = (line.split(','))  # 通过'，'切割
                key = values[0]+'_'+values[1]
                fp = basePath + '有效车辆归类/%s.txt'%key

                f_in = open(fp, "a+",encoding='utf-8',errors='ignore')
                valueLine = key + ',' + values[7] + ',' + values[9] + ',' + values[10] + '\n'
                f_in.write(valueLine)
                f_in.close()
            except:
                pass

def run_yc(basePath):
    rootdir = basePath + 'YuanShiData'
    print(rootdir)
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    print(len(list))
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if str(path).endswith('txt'):
                try:
                    analyze_yc(path,basePath)
                except:
                    fp = basePath + '错误/有效归类错误文件.txt'
                    f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
                    f_in.write(list[i] + '\n')
                    f_in.close()

