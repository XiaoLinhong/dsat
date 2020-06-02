''' 通用函数 '''
import os
import sys

def makedir(fileName):
    ''' 为文件 创建文件夹 '''
    path = os.path.dirname(fileName)
    if not os.path.exists(path):
        os.makedirs(path)

def getsize(fileName):
    ''' 获取文件大小 '''
    if os.path.exists(fileName):
        size = os.path.getsize(fileName)
    else:
        size = 0
    return size

def meter(nowSize, size):
    ''' 显示进度条 '''
    done = int(50 * nowSize / size)
    sys.stdout.write("\r[%s%s] %d%%" % ('█'*done, ' ' * (50-done), 100 * nowSize / size))
    sys.stdout.flush()
