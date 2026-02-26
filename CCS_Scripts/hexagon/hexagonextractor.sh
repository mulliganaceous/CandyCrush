#!/bin/bash
echo Timestamp: ${1}
rm summary*; echo ${1} > $; echo 0 >> $
echo Timestamp: ${1}-0 > summary-0.txt
python3 hexagonextractor.py < $ >> summary-0.txt
rm $; echo ${1} > $; echo 0 >> $
echo Timestamp: ${1}-0 > summary-1.txt
python3 hexagonextractor.py < $ >> summary-1.txt
rm $;
