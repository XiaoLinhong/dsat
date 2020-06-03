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

def get_segmet(outName, size, iterator):
    ''' 迭代下载过程 '''
    makedir(outName)
    nowSize = getsize(outName) # 当前文件大小
    if nowSize == size: # 已经下载完成
        return True
    with open(outName, "wb") as fd:
        try:
            for chunk in iterator:
                if chunk:
                    # print(outName, size, nowSize)
                    nowSize += len(chunk)
                    fd.write(chunk)
                    fd.flush()
                    meter(nowSize, size)
                else:
                    break
        except Exception as err:
            print(err)
            return False
    if nowSize == size:
        print('\n %s is complete! \n' % outName)
        return True
    return True