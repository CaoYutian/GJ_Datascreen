#Author:Sunshine丶天
import os

def analyze(filepath,basepath):
    f_in = open(basepath +'完整停车点.txt', "a+", encoding='utf-8', errors='ignore')
    with open(filepath, "r", encoding='utf-8') as f_out:
        for line in f_out:
            line = line.strip()
            line = line + '\n'
            f_in.write(line)
    f_in.close()

def run_synthetic(basepath):
    rootdir = basepath + '完整停车点'
    list = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    for i in range(0, len(list)):
        path = os.path.join(rootdir, list[i])
        if os.path.isfile(path):
            if str(path).endswith('txt'):
                analyze(path,basepath)
