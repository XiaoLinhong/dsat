import os
import sys
from datetime import datetime,timedelta
import netCDF4 as nc
from netCDF4 import Dataset
from netCDF4 import MFDataset
import xarray as xr


from ..lib import  makedir

NAME = {'L3':'AOT_L2_Mean', 'L2':'AOT',}  #读取变量名，没写完
FREQ = {'1D':'daily','1H':'hourly',} #L3
outPathNAME={'ARP':'A0D','CLP':'CLOUD','WLF':'FIRE'}


def handler(cfg, thisTime, prodocts):
    ''' 下载所有产品 '''
    kargs = dict(satellite='h08', time=thisTime.strftime('%Y%m%d'))
    time  = datetime.strftime(thisTime, '%Y%m%d')
    
    for key in prodocts: # 产品条目
        item = prodocts[key]
        kargs['level'] = item['level']
        inputPath = cfg.rawPath.format(name=item['varName'],**kargs)    
        files     = os.listdir(inputPath)
        
        for file in files:
             if file.endswith('.nc'):                 
                if kargs['level'] == 'L3':
                    file_freq=file[18:20]
                    outPath   = cfg.outPath.format(name=outPathNAM[item['varName']],freq=FREQ[file_freq],**kargs)
                if kargs['level'] == 'L2':
                    outPath   = cfg.outPath.format(name=outPathNAM[item['varName']],freq='minutly',**kargs)
                ifile = inputPath + os.sep  + file
                ofile = outPath + os.sep  + get_newname(file,kargs['level'])
                print(ifile)                
                print(ofile)
                if not os.path.exists(ofile):
                    read_nc(ifile, ofile,kargs['level'])
                    print('ok')
def read_nc(ifile,ofile,levename):
        fh = xr.open_dataset(ifile)
        AOT = fh[NAME[levename]]  
        latitude = fh['latitude']
        longitude = fh['longitude']
        makedir(ofile)
        xr.Dataset({'latitude':latitude,'longitude':longitude,'AOT':AOT}).to_netcdf(ofile)

def get_newname(filename,levename):
    if levename == 'L3':
       satellite   =filename[0:3]
       itime       =filename[4:12]+'_'+filename[13:17]
       newFileName = satellite+'_'+levename+'_'+ itime +'.nc'
    elif levename == 'L2':
       satellite   =filename[3:6]
       itime       =filename[7:15]+'_'+filename[16:20]
       newFileName = satellite+'_'+levename+'_'+ itime +'.nc'

    return(newFileName)
