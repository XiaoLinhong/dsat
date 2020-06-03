set -e # stop the shell on first error

#多天循环下载
BegTime=$(date -d"2019-01-01" '+%s')
EndTime=$(date -d"2019-12-31" '+%s')

# 执行下载循环
while [ $BegTime -le $EndTime ]; do
    thisTime=$(date -d@${BegTime} +%Y%m%d)
    python -m dsat -t $thisTime -s h08
    python -m dsat -t $thisTime -s sent
    python -m dsat -t $thisTime -s viirs
    let BegTime=BegTime+24*3600
done

