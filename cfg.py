# 需要下载的卫星产品
products = {
    'viirs': {
            'aod': {
                'AERDB': ['D3', 'L2'],  #日均的数据，时效性比较低，大概滞后5天左右
                'AERDT': ['L2'],
             },
    },
    'sent': { # 'L2__CH4'
        'Sentinel-5': ['L2__CLOUD_', 'L2__CO____', 'L2__HCHO__', 'L2__NO2___', 'L2__O3_TCL', 'L2__O3____', 'L2__SO2___', 'L2__O3__PR'],
    },
    'h08': { # 小时和日均
        'd1': dict(level='L3', varName='ARP', algorithm='030'), # 气溶胶
        'd2': dict(level='L2', varName='ARP', algorithm='021'), # 气溶胶
    },
}
