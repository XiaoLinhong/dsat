''' 加载配置信息 '''
import os
import sys
import types
from argparse import ArgumentParser
from datetime import datetime, timedelta

PATH = os.path.split(os.path.realpath(__file__))[0]
HOME = os.path.dirname(PATH) # 获取项目家目录

def get_dynamic_params():
    ''' get the dynamic parameter'''
    parser = ArgumentParser(description='Satellite environmental data products')
    # description of parameters
    parser.add_argument('-f', '--fileName', type=str, default='cfg.py', help='Name of configue file')
    parser.add_argument('-t', '--thisTime', type=str, default='20200531', help='Day of downloading')
    parser.add_argument('-s', '--satellite', type=str, default='viirs', help='viirs h08(葵花) sent(哨兵)')

    args = parser.parse_args()

    fileName = args.fileName
    thisTime = args.thisTime
    satellite = args.satellite
    try:
        thisTime = datetime.strptime(thisTime, '%Y%m%d')
    except Exception as err:
        print(err, 'given wrond time')
        exit(1)
    return fileName, thisTime, satellite

class cfg:
    ''' 配置对象 '''
    products = {}

def load_cfg():
    ''' 加载用python语法写的配置文件 '''
    fileName, thisTime, satellite = get_dynamic_params()
    try:
        cfgModule = types.ModuleType("cfg")
        code = open(fileName, encoding='utf-8').read()
        exec(code, cfgModule.__dict__)
    except Exception as err:
        print(err, fileName)
        sys.exit(1)

    for name in dir(cfgModule): # 将挂载在模块上面的属性，负值给cfg类
        if not name.startswith('_'):
            setattr(cfg, name, getattr(cfgModule, name))
    cfg.thisTime = thisTime
    cfg.satellite = satellite
    # 内部配置: 世界时间，还是北京时间
                                   # 卫星      产品级别 产品名称 时间
    cfg.rawName = HOME + '/data/raw/{satellite}/{level}/{name}/{time}/{file}'.replace('/', os.sep)
    cfg.outName = HOME + '/data/out/{varName}/{freq}/{time}/{satellite}_{level}_{YMDH}.nc'.replace('/', os.sep)
    cfg.done = HOME + '/data/log/{satellite}_{time}_done'.format(satellite=satellite, time=thisTime.strftime('%Y-%m-%d'))
    cfg.rawPath = HOME + '/data/raw/{satellite}/{level}/{name}/{time}'.replace('/', os.sep)
    cfg.outPath =  HOME + '/data/out/{name}/{freq}/{time}'.replace('/', os.sep)
    return cfg
