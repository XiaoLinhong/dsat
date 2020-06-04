''' 哨兵卫星数据产品 '''

import os
from datetime import timedelta

import requests
from requests import Session
from requests.auth import HTTPBasicAuth


from ..lib import getsize, makedir, get_segmet

LOGIN = 'https://s5phub.copernicus.eu/dhus////login' # 登录表单地址
QUARRY = 'https://s5phub.copernicus.eu/dhus/api/stub/products' # 产品查询地址
URL = "https://s5phub.copernicus.eu/dhus/odata/v1/Products('{uuid}')/$value" # 产品下载地址

PARAMS = {
    'filter': '(ingestionDate:[{begTime} TO {endTime}]) AND (platformname:{version} AND producttype:{varName})',
    'offset': 0,
    'limit': 25,
    'sortedby': 'ingestiondate',
    'order': 'desc',
}

FORM = {"login_username": 's5pguest',
        "login_password": 's5pguest',
}
login = 's5pguest'
password = 's5pguest'
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def download(cfg, thisTime, prodocts):
    ''' 下载所有产品 '''
    kargs = dict(satellite='sent', time=thisTime.strftime('%Y%m%d'))
    for version in prodocts: # 目前只支持哨兵5
        for varName in prodocts[version]: # 不同变量产品
            cols = varName.split('_') # 解析产品级别和变量名 'L2__O3____'
            productLists = get_product_lists(version, varName, thisTime) # 查询ID
            for item in productLists:
                outName = cfg.rawName.format(level=cols[0], name=cols[2], file=item['identifier']+'.nc', **kargs)
                for i in range(5):
                    print('%s: %d th attempt' % (os.path.basename(outName), (i+1)))
                    flag = download_one_product(item['uuid'], outName)
                    if flag: break
                    if not flag and os.path.exists(outName): # 下载失败，删除破碎文件
                        os.remove(outName)

def get_product_lists(version, varName, thisTime, params=PARAMS):
    ''' 获取哨兵卫星当日的产品 '''
    begTime = thisTime.strftime('%Y-%m-%dT00:00:00.000Z')
    endTime = (thisTime + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00.000Z')

    params['filter'] = params['filter'].format(begTime=begTime, endTime=endTime, varName=varName, version=version)
    with Session() as session:
        session.post(LOGIN, data=FORM, auth=HTTPBasicAuth(login, password), headers=headers)
        response = session.get(QUARRY, params=params)
        content = response.json()
        products = []
        for item in content['products']:
            product = {
                'identifier': item['identifier'],
                'uuid': item['uuid'],
            }
            products.append(product)
        return products

def download_one_product(uuid, outName):
    ''' 下载一个产品 '''
    url = URL.format(uuid=uuid)

    with Session() as session:
        session.post(LOGIN, data=FORM, auth=HTTPBasicAuth(login, password), headers=headers)
        try: # url加载问题
            response = session.get(url, stream=True, verify=False)
        except:
            print('Please check if %s is right' % url)
            return False
        size = int(response.headers['Content-Length']) # 文件大小
        iterator = response.iter_content(chunk_size=1024)
        return get_segmet(outName, size, iterator)
