#Author:Sunshine丶天
import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from core import main

if __name__ == '__main__':
    # 全代码控制linux服务器 自动分析数据
    roorPath = '/data/030/Data_' + sys.argv[1] + '/'
    main.run(roorPath)



