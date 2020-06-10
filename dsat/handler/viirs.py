''' viirs 卫星产品下载 '''
import os
from datetime import datetime,timedelta
import time
import xarray as xr
import netCDF4 as nc
from netCDF4 import Dataset
from netCDF4 import MFDataset

from ..lib import getsize, makedir, get_latlon

NAME = {'D3':'Aerosol_Optical_Thickness_550_Land_Ocean_Mean', 'L2':'Aerosol_Optical_Thickness_550_Land_Ocean',}
FREQ = {'D3':'daily','L2':'minutly',}
def handler(cfg, thisTime, prodocts):
    ''' VIIRS数据处理'''
    for key in prodocts: # 变量
        for algorithm in prodocts[key]: # 算法
            for level in prodocts[key][algorithm]: # 产品级别
                params = dict(satellite='viirs', level=level)
                inputPath = cfg.rawPath.format(name=algorithm,time=thisTime.strftime('%Y%m%d'),**params)
                files = os.listdir(inputPath)
                for file in files:
                    if file.endswith('.nc'): 
                        outTime = (datetime.strptime(file[21:28],'%Y%j')).strftime('%Y%m%d')
                        outPath = cfg.outPath.format(name='AOD',freq=FREQ[level],time=outTime,**params)
                        ifile = inputPath + os.sep  + file
                        ofile = outPath + os.sep  + get_newname(file)
                        if get_latlon(ifile) and not os.path.exists(ofile):
                            read_nc(ifile, ofile, level)
                print('ok')

def read_nc(ifile, ofile, varName):
       makedir(ofile)
       datas     = xr.open_dataset(ifile)
       AOT       = datas[NAME[varName]]
       latitude  = datas['Latitude']
       longitude = datas['Longitude']
       xr.Dataset({'latitude':latitude,'longitude':longitude,'AOT':AOT}).to_netcdf(ofile)


def get_newname(filename):
       satellite = filename[9:14]
       algorithm = filename[0:5]
       itime     = (datetime.strptime(filename[21:28],'%Y%j')).strftime('%Y%m%d')+'_'+filename[29:33]
       newFileName = satellite+'_'+algorithm+'_'+itime+'.nc'
       return(newFileName)
 




