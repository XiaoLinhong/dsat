set -e # stop the shell on first error

#多天循环下载
BegTime=$(date -d"2020-05-25" '+%s')
EndTime=$(date -d"2020-05-26" '+%s')

# 执行下载循环
while [ $BegTime -le $EndTime ]; do
    thisTime=$(date -d@${BegTime} +%Y%m%d)
    python -m dsat -t $thisTime
    let BegTime=BegTime+24*3600
done

