''' 通用函数 '''
import os
import sys
import xarray as xr
def touch(fileName):
    ''' 写一个空文件 '''
    makedir(fileName)
    with open(fileName, 'w') as fh:
        pass

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
    sys.stdout.write("\r[%s%s] %d%%" % ('\033[42m \033[0m'*done, ' ' * (50-done), 100 * nowSize / size))
    #sys.stdout.write("\r[%s%s] %d%%" % ('█'*done, ' ' * (50-done), 100 * nowSize / size))
    sys.stdout.flush()

def get_segmet(outName, size, iterator):
    ''' 迭代下载过程 '''
    makedir(outName)
    nowSize = getsize(outName) # 当前文件大小
    if nowSize == size: # 已经下载完成
        return True
    
    if nowSize != size and nowSize > 0:
        os.remove(outName)       
        nowSize = 0

    with open(outName, "wb") as fd:
        try:
            for chunk in iterator:
                if chunk:
                    nowSize += len(chunk)
                    fd.write(chunk)
                    fd.flush()
                    meter(nowSize, size)
                else:
                    if nowSize == size:
                        break
        except Exception as err:
            print(err)
            return False
    if nowSize == size:
        print('\n %s is complete! \n' % os.path.dirname(outName))
        return True
    return False

def get_latlon(position):
    ###读取数据经纬度最值,并输出NC文件
    datas = xr.open_dataset(position)
    lat_min=datas.attrs['geospatial_lat_min']
    lat_max=datas.attrs['geospatial_lat_max']
    lon_min=datas.attrs['geospatial_lon_min']
    lon_max=datas.attrs['geospatial_lon_max']
    if (lat_min>0 and lat_min<55) or (lat_max>0 and lat_max<55) or (lon_min>72 and lon_min<136) or (lon_max>72 and lon_max<136):
       return True

