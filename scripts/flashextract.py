"""
A script which extracts the configs of the Flash version of CCS.
The Flash version still exists, including potential worlds after World 53.
Note all worlds after World 53 have three episodes.\

Author: Mulliganaceous
"""

import urllib.request
from urllib.error import HTTPError

def extractworld(data, offset:int, note=""):
    """
    Extract all the worlds starting from world 1 + offset.
    The world number is given by offset+count.
    """
    count = 0
    world, hasworld = offset, True
    while (hasworld):
        try:
            count += 1
            res = urllib.request.urlopen("https://d1s72spon8oqz4.cloudfront.net/resources/game-configurations{0:d}.json".format(offset+count))
            body = res.read()
            data = data + body.decode().replace('\\"', '"').replace('"{', '{').replace('}"', '}').lstrip('[').rstrip(']') + ","
            print("World {0:d} extracted.".format(offset+count))
        except HTTPError:
            print("Total of {0:d} {1:s} worlds extracted on the Flash version.".format(count-1, note))
            hasworld = False
    return data

data = extractworld("", 0, "Re")
data = extractworld(data, 1200, "Dw")

f = open("CCS_Flash_configs.json", "w")
f.write("[" + data.rstrip(",") + "]")
f.close()
