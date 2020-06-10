''' 哨兵卫星数据产品 '''

import os
from datetime import datetime,timedelta

import xarray as xr
import netCDF4 as nc
from netCDF4 import Dataset
from netCDF4 import MFDataset

from ..lib import makedir, get_latlon

NAME = {'L2__O3____':'ozone_total_vertical_column', 'L2__CLOUD_':'cloud_fraction',}

def handler(cfg, thisTime, prodocts):
    '''哨兵卫星数据处理 '''
    kargs = dict(satellite='sent')
    #kargs = dict(satellite='sent', time=thisTime.strftime('%Y%m%d'))
    inputTime=thisTime.strftime('%Y%m%d')
    for varName in prodocts['Sentinel-5']: # 不同变量产品
        cols = varName.split('_') # 解析产品级别和变量名 'L2__O3____'
        inputPath = cfg.rawPath.format(level=cols[0], name=cols[2], time=inputtime,**kargs)
     #   outPath = cfg.outPath.format(name=cols[2], freq='hourly', **kargs)
        files = os.listdir(inputPath)
        for file in files:
            if file.endswith('.nc'):  
                outTime = file[20:28]
                outPath = cfg.outPath.format(name=cols[2], freq='hourly',time=outTime, **kargs)
                ifile = inputPath + os.sep  + file
                ofile = outPath + os.sep  + get_newname(file)
                if get_latlon(ifile) and not os.path.exists(ofile):
                    read_nc(ifile, ofile, varName)
                                    
def read_nc(ifile, ofile, varName):
      ''' 读入原始文件需要的变量，重新输出 '''
      fh = Dataset(ifile, mode='r')
      lons_fh = fh.groups['PRODUCT'].variables['longitude'][:][0,:,:]
      lats_fh = fh.groups['PRODUCT'].variables['latitude'][:][0,:,:]
      data_fh = fh.groups['PRODUCT'].variables[NAME[varName]][:][0,:,:]
      data_fh_units = fh.groups['PRODUCT'].variables[NAME[varName]].units
      # 创建新NC文件
      makedir(ofile)
      da = nc.Dataset(ofile, 'w', format='NETCDF4')
      # 创建nc文件中dimension
      da.createDimension('scanline', (lons_fh.shape[0]))
      da.createDimension('ground_pixel', (lons_fh.shape[1]))
      # 创建文件变量
      lons = da.createVariable('lons', 'f4', ('scanline','ground_pixel'))
      lats = da.createVariable('lats', 'f4', ('scanline','ground_pixel'))
      data = da.createVariable(NAME[varName], 'f4', ('scanline','ground_pixel'))
      lons[:,:] = lons_fh[:,:]
      lats[:,:] = lats_fh[:,:]
      data[:,:] = data_fh[:,:]
      # 对nc文件增加说明变量
      lats.units = 'degrees north'
      lons.units = 'degrees east'
      data.units = data_fh_units
      da.close()

def get_newname(filename):
       satellite = filename[0:3]
       leve      = filename[9:11]
       itime     = filename[20:28] + '_' + filename[29:33] # yyyymmdd_hhmm
       newFileName = satellite +'_' + leve + '_'+ itime +'.nc'
       return(newFileName)

