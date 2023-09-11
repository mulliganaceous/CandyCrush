"""
A script which extracts the configs of a CCS config folder of zip, then
combines it into a single JSON file.

Author: Mulliganaceous
Version: 1.1
Date: 2022 Sep 26
"""

import os
import re
import urllib.request
from urllib.error import HTTPError
import zipfile
from datetime import datetime
import json

INTERVAL = 75
FBFOLDER = "fb/"

def extract_folder(path, outputname=None):
    print("Extracting and converting folder...")
    configlist = os.listdir(path)
    regex = re.compile('episode(\d*)level(\d*)\.txt')
    for k in range(len(configlist)):
        matched = regex.match(configlist[k])
        if matched:
            configlist[k]=(">episode{0:04d}level{1:02d}.txt".format(int(matched.group(1)), int(matched.group(2))))
    configlist.sort()

    data = None
    totalLevel = 0
    realityLevel = 0
    f = None
    if not outputname:
        outputname = path
    g = open(outputname + ".json", 'w')
    regex = re.compile('>episode(\d*)level(\d*)\.txt')
    g.write('[')
    for config in configlist:
        if totalLevel > 0:
            g.write(',\n')
        matched = regex.match(config)
        if matched:
            f = open(path + "/episode{0:d}level{1:d}.txt".format(int(matched.group(1)), int(matched.group(2))),'r')
            data = '{' + '"episode":{0:d},"level":{1:d},"sequence":{2:d},"gameData":{3:s}'.format(int(matched.group(1)), int(matched.group(2)), realityLevel + 1, f.read()) + '}'
            f.close()
            if realityLevel % INTERVAL == 0:
                print('\t' + config)
            realityLevel += 1
        elif config[-4:] == ".txt":
            try:
                f = open(path + "/{0:s}".format(config))
                data = '{' + '"episode":0,"level":0,"sequence":"{0:s}","gameData":{1:s}'.format(config, f.read()) + '}'
                f.close()
            except:
                pass
            print('\t' + config)
        totalLevel += 1
        g.write(data)
        
    g.write(']')
    print("Extracted {0:d} ({1:d}) config txt files.".format(totalLevel, realityLevel))
    g.close()

def extract_zip(path, outputname=None, headerjson = {}):
    print("Extracting and converting zip file...")
    totallevel, realitylevel = 0, 0
    if not outputname:
        outputname = path[:-4]
    g = open(outputname + ".json", 'w')

    g.write('[' + str(headerjson))
        
    z = zipfile.ZipFile(path, 'r')
    namelist = z.namelist()
    regex = re.compile('levels/episode(\d*)level(\d*)\.txt')
    for k in range(len(namelist)):
        matched = regex.match(namelist[k])
        if matched:
            namelist[k]=(">episode{0:04d}level{1:02d}.txt".format(int(matched.group(1)), int(matched.group(2))))
    namelist.sort()
    
    
    regex = re.compile('>episode(\d*)level(\d*)\.txt')
    data = None
    for config in namelist:
        g.write(',\n')
        matched = regex.match(config)
        if matched:
            configpath = "levels/episode{0:d}level{1:d}.txt".format(int(matched.group(1)), int(matched.group(2)))
            gamedata = z.read(configpath).decode(encoding='utf-8', errors='strict')
            data = '{' + '"episode":{0:d},"level":{1:d},"sequence":{2:d},"gameData":{3:s}'.format(int(matched.group(1)), int(matched.group(2)), realitylevel + 1, gamedata) + '}'
            realitylevel += 1
            if realitylevel % INTERVAL == 0:
                print('\t' + config)
        elif config[-4:].endswith(".txt"):
            gamedata = z.read(configpath).decode(encoding='utf-8', errors='strict')
            if config.startswith("levels/"):
                config = config[7:]
            data = '{' + '"episode":0,"level":0,"sequence":"{0:s}","gameData":{1:s}'.format(config, gamedata) + '}'
            print('\t' + config)
        totallevel += 1
        g.write(data)
        
    g.write('\n]')
    print("Extracted {0:d} ({1:d}) config txt files.".format(totallevel, realitylevel))
    g.close()

def extract_fb():
    """
    Extract all worlds from the zip file.
    """
    print("Extracting and converting master config files online...")
    count = 0
    try:
        # Perform request
        res = urllib.request.urlopen("https://king-candycrush-prod.secure2.footprint.net/client/semi_group_levels.zip")
        # Download file
        print(res.headers.get('Date'))
        print(res.headers.get('Last-Modified'))
        headerjson = json.JSONEncoder().encode(dict(res.headers.items()))
        path = "semi_group_levels_{0:s}".format(datetime.strptime(res.headers.get('Last-Modified'), "%a, %d %b %Y %H:%M:%S %Z").strftime("%y%m%d.%H%M%S%a"))
        f = open(FBFOLDER + path + ".zip", 'wb')
        f.write(res.read())
        print("Downloaded config file")
        f.close()
        # Perform zip
        extract_zip(FBFOLDER + path + ".zip", path, headerjson)
    except HTTPError:
        print("Failed to extract semi_group_levels.zip")
    finally:
        print(res)
        print(res.headers)

##extract_folder('zips/master')
##extract_zip('zips/1dwf0s8.zip')
##extract_zip('zips/6d97bb6b76adc61d42a20184af5f5bfb9a55fad4_60596_leveltweaks123608_20220923134143_0_all.zip', 'zips/tweaks')
extract_fb()
