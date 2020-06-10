''' 评估程序主模块 '''

from .configure import load_cfg

from . import download

from . import handler

from .lib import touch

def main():
    ''' 主程序 '''
    # 加载配置
    cfg = load_cfg()

    # 下载卫星数据
    #print(cfg.thisTime)
    if not os.path.exists(cfg.done): 
       for i in range(20):
           flag = getattr(download, cfg.satellite).download(cfg, cfg.thisTime, cfg.products[cfg.satellite])
           if flag: # 成功下载
               touch(cfg.done)
               break 
           else:
               print('download time:', i)
               print('Resubmit the download task')
    else:
    # 处理数据
       getattr(handler, cfg.satellite).handler(cfg, cfg.thisTime, cfg.products[cfg.satellite]) 
