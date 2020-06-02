''' viirs 卫星产品下载 '''

import requests

from ..lib import getsize, makedir, meter

URL = "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5110/"
NAME = "{algorithm}_L2_VIIRS_SNPP/{year}/{julDay:03d}"

def get_targets(thisTime, outName, algorithm='AERDT'):
    ''' 获取一天中所有的文件 '''
    targets = {} # 返回值
    params = dict(satellite='viirs', level='L2', name=algorithm, time=thisTime.strftime('%Y%m%d'))
    
    url = URL + NAME.format(algorithm=algorithm, year=thisTime.year, julDay=int(thisTime.strftime('%j')))
    response = requests.get(url+'.json')
    if not response.ok:
        print('Please check if this url(%s) is right!' % response.url)
        exit(1)
    # 用json格式解析http返回
    content = response.json()

    for item in content:
        params['file'] = item['name'] # 输出原始文件名
        thisFile = outName.format(**params)
        nowSize = getsize(thisFile)
        if nowSize != item['size']: # 跳过已完成下载的文件
            targets[thisFile] = dict(url=url+'/'+item['name'], size=item['size'], nowSize=nowSize)
    return targets

def download(cfg, thisTime, prodocts):
    ''' 下载 '''
    for key in prodocts: # 变量
        for algorithm in prodocts[key]:
            targets = get_targets(thisTime, cfg.rawName, algorithm)
            for outName in targets: # 下载一个文件
                for i in range(5):
                   print('%s: %d th attempt' % (outName, (i+1)))
                   flag = download_one(outName=outName, **targets[outName])
                   if flag: break
                if not flag: # 下载失败，删除破碎文件
                   if os.path.exists(outName): os.remove(outName)
                   
def download_one(url, size, nowSize, outName):
    ''' 下载一个文件 '''
    headers = {'Authorization': 'Bearer 55F841D4-88FE-11EA-9FE6-AEB2F2747E3F'}
    try: # url加载问题
        response = requests.get(url, timeout=5, stream=True, headers=headers)
    except:
        print('Please check if %s is right' % url)
        return False
    makedir(outName)
    with open(outName, "wb") as fd:
        try:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    # print(outName, size, nowSize)
                    nowSize += len(chunk)
                    fd.write(chunk)
                    fd.flush()
                   # meter(nowSize, size)
        except:
            return False
    if nowSize == size:
        print('%s is complete!' % outName)
        return True