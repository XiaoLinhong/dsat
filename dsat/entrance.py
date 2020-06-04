''' 评估程序主模块 '''

from .configure import load_cfg

from . import download

def main():
    ''' 主程序 '''
    # 加载配置
    cfg = load_cfg()

    # 下载卫星数据
    getattr(download, cfg.satellite).download(cfg, cfg.thisTime, cfg.products[cfg.satellite])

    # 处理数据
   
