import os
import sys

from ftplib import FTP

from ..lib import getsize, makedir, get_segmet


HOST = "ftp.ptree.jaxa.jp"

FORM = dict(
    username="liangqian1995_126.com",
    password="SP+wari8",
)

# lftp liangqian1995_126.com:SP+wari8@ftp.ptree.jaxa.jp

PATH = dict(
    hourly="/pub/himawari/{level}/{varName}/{algorithm}/%Y%m/%d/",
    daily="/pub/himawari/{level}/{varName}/{algorithm}/%Y%m/daily/"
)


def get_ftp(username, password, host=HOST, port=21):
    ''' 获取ftp链接 '''
    ftp = FTP()
    try:
        ftp.connect(host, port)
        ftp.login(username, password)
    except Exception as err:
        print("FTP登陆失败，请检查主机号、用户名、密码是否正确", err)
        sys.exit(1)

    ftp.voidcmd('TYPE I')
    return ftp

def get_ftp_fileName(item, path, thisTime):
    ''' 获取当前时间所有文件名'''
    ftp = get_ftp(**FORM)
    thisPath = thisTime.strftime(path).format(**item)
    try:
        fileNames = ftp.nlst(thisPath)
    except Exception as err:
        print(err)
    if fileNames[0].endswith('nc'): # level 3
        return fileNames
    if fileNames[0].endswith('csv'): # level 3
        return fileNames
    files = [] # level 2
    for path in fileNames:
        files += ftp.nlst(path)
    return files

def download(cfg, thisTime, prodocts):
    ''' 下载所有产品 '''
    yesno = True
    kargs = dict(satellite='h08', time=thisTime.strftime('%Y%m%d'))
    for key in prodocts: # 产品条目
        item = prodocts[key]
        kargs['level'], kargs['name'] = item['level'], item['varName']
        for freq in PATH:
            if item['level'] == 'L2' and freq == 'daily': continue
            fileNames = get_ftp_fileName(item, PATH[freq], thisTime) # 获取所有远程文件路径
            for remoteName in fileNames:
                outName = cfg.rawName.format(file=os.path.basename(remoteName), **kargs)
                for i in range(5):
                    print('%s: %d th attempt' % (os.path.basename(outName), (i+1)))
                    flag = download_one_product(remoteName, outName)
                    if flag: 
                        break
                    else:
                        if os.path.exists(outName): os.remove(outName) # 下载失败，删除破碎文件
                if i == 4 and not flag:
                    yesno = False
    return yesno           
def download_one_product(remoteName, outName):
    ''' 下载一个文件 '''
    ftp = get_ftp(**FORM)
    size = ftp.size(remoteName)
    try: # url加载问题
        connect = ftp.transfercmd('RETR {file}'.format(file=remoteName))
    except:
        print('Please check if %s is right' % remoteName)
        return False
    iterator = iter(FtpIiterator(connect))
    return get_segmet(outName, size, iterator)

class FtpIiterator:
    ''' FTP下载迭代器 '''

    def __init__(self, connect, buffer=1024):
        self.buffer = buffer
        self.connect = connect

    def __iter__(self):
        return self
 
    def __next__(self):
        chunk = self.connect.recv(self.buffer)
        if chunk:
            return chunk
        else:
            raise StopIteration
