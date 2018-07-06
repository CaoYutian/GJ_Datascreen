#Author:Sunshine丶天
import os

def getcarlist(basepath):

    rootdir = basepath + '停车点'
    lists = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件

    fp = basepath + 'carlist.txt'
    f_in = open(fp, "a+", encoding='utf-8', errors='ignore')

    for list in lists:
        if str(list).endswith('txt'):
            arr = list.split('.')
            valueLine = arr[0] + '\n'
            f_in.write(valueLine)

    f_in.close()