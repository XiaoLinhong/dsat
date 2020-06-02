''' 哨兵卫星数据产品 '''

import os
from datetime import timedelta

import requests
from requests import Session

from ..lib import getsize, makedir, meter


varName = ['L2__CH4', 'L2__CLOUD_', 'L2__CO____', 'L2__HCHO__', 'L2__NO2___',
           'L2__O3_TCL', 'L2__O3____', 'L2__SO2___', 'L2__O3__PR', ]

LOGIN = 'https://s5phub.copernicus.eu/dhus////login'
QUARRY = 'https://s5phub.copernicus.eu/dhus/api/stub/products'
URL = "https://s5phub.copernicus.eu/dhus/odata/v1/Products('{uuid}')/$value"

PARAMS = {
    'filter': '(ingestionDate:[{begTime} TO {endTime}]) AND (platformname:Sentinel-5 AND producttype:{varName})',
    'offset': 0,
    'limit': 25,
    'sortedby': 'ingestiondate',
    'order': 'desc',
}

FORM = {"login_username": 's5pguest',
         "login_password": 's5pguest',
        }

def download(cfg, thisTime, prodocts):
    ''' 下载 '''
    varName = 'L2__O3____' # 解析变量；
    productLists = get_product_lists(varName, thisTime)
    for item in productLists:
        download_one_product(item['uuid'], cfg.rawName, thisTime, level='L2', name='O3')
    print(productLists)

def get_product_lists(varName, thisTime, params=PARAMS):
    ''' 获取哨兵卫星当日的产品 '''

    begTime = thisTime.strftime('%Y-%m-%dT00:00:00.000Z')
    endTime = (thisTime + timedelta(days=1)).strftime('%Y-%m-%dT00:00:00.000Z')

    params['filter'] = params['filter'].format(begTime=begTime, endTime=endTime, varName=varName)
    with Session() as session:
        session.post(LOGIN, data=FORM)
        response = session.get(QUARRY, params=params)
        content = response.json()
        products = []
        for item in content['products']:
            product = {
                'identifier': item['identifier'],
                'uuid': item['uuid'],
                'date': item['summary'][0][7:-14]
            }
            products.append(product)
        return products

def download_one_product(uuid, outName, thisTime, level='L2', name='O3'):
    ''' 下载一个产品 '''
    url = URL.format(uuid=uuid)

    with Session() as session:
        session.post(LOGIN, data=FORM)
        try: # url加载问题
            response = session.get(url, stream=True, verify=False)
        except:
            print('Please check if %s is right' % url)
            return False
        fileName = response.headers['Content-Disposition'][17:-1] # 获取文件名
        thisName = outName.format(satellite='sent', level=level, name=name, time=thisTime.strftime('%Y%m%d'), file=fileName)
        makedir(thisName)
        size = int(response.headers['Content-Length']) # 文件大小
        nowSize = getsize(fileName) # 单前文件大小
        with open(thisName, "wb") as fd:
            try:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        print(thisName, size, nowSize)
                        nowSize += len(chunk)
                        fd.write(chunk)
                        fd.flush()
            except:
                return False
        if nowSize == size:
            print('%s is complete!' % thisName)
            return True