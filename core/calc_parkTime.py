#Author:Sunshine丶天
# -*- coding: utf-8 -*-
# 计算停车时长
from math import sin, asin, cos, radians, fabs, sqrt
import os
import datetime
import threading
import multiprocessing

EARTH_RADIUS = 6371  # 地球平均半径，6371km

def hav(theta):
    s = sin(theta / 2)
    return s * s

# 计算距离
def get_distance_hav(lat0, lng0, lat1, lng1):
    "用haversine公式计算球面两点间的距离。"
    # 经纬度转换成弧度
    lat0 = radians(lat0)
    lat1 = radians(lat1)
    lng0 = radians(lng0)
    lng1 = radians(lng1)

    dlng = fabs(lng0 - lng1)
    dlat = fabs(lat0 - lat1)
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)
    distance = 2 * EARTH_RADIUS * asin(sqrt(h)) * 1000

    return distance

#经纬度格式化
def conversionLon(lonStr):
    if (int(lonStr[0:1]) == 1):
        longitude = float(lonStr[0:9]) / 1000000
    else:
        longitude = float(lonStr[0:8]) / 1000000
    try:
        return longitude
    except:
        print('经纬度出错了')

def conversionLat(latStr):
    latitude = float(latStr[0:8]) / 1000000
    try:
        return latitude
    except:
        print('经纬度出错了')

# 计算时间差 输出分钟差
def time_differ(date1,date2):
    # @传入是时间格式如'12:55:05'
    date1=datetime.datetime.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2=datetime.datetime.strptime(date2,"%Y-%m-%d %H:%M:%S")
    if date1 < date2:
        secondsDiff = (date2 - date1).seconds
        daysDiff = (date2 - date1).days
        minutesDiff = daysDiff * 1440 + round(secondsDiff / 60, 1)
        return minutesDiff
    else:
        secondsDiff = (date1 - date2).seconds
        daysDiff = (date1 - date2).days
        minutesDiff = daysDiff * 1440 + round(secondsDiff / 60, 1)

        return minutesDiff

def analyze(filepath,basePath,str_name):
    sourceArr = []
    with open(filepath, 'r', encoding='utf-8') as f_out:
        for line in f_out:
            line = line.strip()
            sourceArr.append(line)

        # 第一条数据 获取首位经纬度
        firstLine = sourceArr[0].split(',')
        if len(firstLine) == 4:
            currentLon = conversionLon(firstLine[2])
            currentLat = conversionLat(firstLine[3])

            indexTotalStr = '0'
            for i in range(len(sourceArr)):
                # 每行数据通过逗号切割
                LineArr = sourceArr[i].split(',')

                # 下一个比对的经纬度
                nextLon = conversionLon(LineArr[2])
                nextLat = conversionLat(LineArr[3])

                # 距离
                Distance = get_distance_hav(currentLat, currentLon, nextLat, nextLon)
                if Distance <= 30:
                    indexTotalStr = '%s,%s' % (indexTotalStr, i)
                else:
                    currentLon = nextLon
                    currentLat = nextLat
                    indexTotalStr = '%s*%s' % (indexTotalStr, i)

            fp = basePath + str_name + firstLine[0] + '.txt'
            arr = indexTotalStr.split('*')

            for sectionStr in arr:
                if len(sectionStr) > 2:
                    array = sectionStr.split(',')
                    # 获取 时间段间的开头和结尾下标
                    startTimeIndex = int(array[0])
                    endTimeIndex = int(array[-1])

                    # 通过 ，切割字符串 在通过数组下标获得需要的信息
                    startArr = sourceArr[startTimeIndex].split(',')
                    endArr = sourceArr[endTimeIndex].split(',')

                    lonS = 0
                    latS = 0
                    for j in range(startTimeIndex, endTimeIndex):
                        line_arr = sourceArr[j].split(',')
                        lonS += int(line_arr[2])
                        latS += int(line_arr[3])

                    # 经纬度平均值
                    if endTimeIndex - startTimeIndex > 0:
                        averageLon = lonS / (endTimeIndex - startTimeIndex)
                        averageLat = latS / (endTimeIndex - startTimeIndex)
                        startArr[2] = int(averageLon)
                        startArr[3] = int(averageLat)

                    differ = time_differ(startArr[1], endArr[1])

                    # +++++++++++设置停车时间间隔时长 （分钟）+++++++++++
                    if differ >= 2:
                        startArr.append(differ)
                        String = ','.join(str(i) for i in startArr) + '\n'
                        f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
                        # 文件写入
                        f_in.write(String)
                        f_in.close()

def run_yc(basePath,count,allCount):
    rootdir = basePath + '排序后车辆'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    start_index = int(len(list) * count / allCount)
    end_index = int(len(list) * (count + 1) / allCount)

    for i in range(start_index, end_index):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if str(path).endswith('txt'):
                try:
                    analyze(path,basePath,'停车点/')
                except:
                    fp = basePath + '错误/停车点错误文件.txt'
                    f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
                    f_in.write(list[i] + '\n')
                    f_in.close()

# ============================ 分割线 ============================
def run_all(basePath,count,allCount):
    rootdir = basePath + '完整排序后车辆'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    start_index = int(len(list) * count / allCount)
    end_index = int(len(list) * (count + 1) / allCount)

    for i in range(start_index, end_index):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if str(path).endswith('txt'):
                try:
                    analyze(path,basePath,'完整停车点/')
                except:
                    fp = basePath + '错误/完整停车点错误文件.txt'
                    f_in = open(fp, "a+", encoding='utf-8', errors='ignore')
                    f_in.write(list[i] + '\n')
                    f_in.close()

def run_parkTime(basePath,type,threadCount):
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