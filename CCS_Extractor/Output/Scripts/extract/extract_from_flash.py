"""
A script which extracts the configs of the Flash version of CCS, then combines
into a single JSON file.

No input arguments are required; just have a good internet connection.

The Flash version still exists, including potential worlds after World 53.
Note all worlds after World 53 have three episodes.

THIS CODE IS ARCHIVED. THE FLASH SITE IS ENTIRELY REMOVED, AFTER STAYING
FOR ABOUT A YEAR SINCE THE DEMISE OF FLASH.

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
    # Perform loop until the first nonrevealed world is reached.
    while (hasworld):
        try:
            count += 1
            res = urllib.request.urlopen("https://d1s72spon8oqz4.cloudfront.net/resources/game-configurations{0:d}.json".format(offset+count))
            body = res.read()
            # The second and third replacements convert gameData fields from JSON strings to JSON objects. 
            data = data + body.decode().replace('\\"', '"').replace('"{', '{').replace('}"', '}').lstrip('[').rstrip(']') + ","
            print("World {0:d} extracted.".format(offset+count))
        except HTTPError:
            print("Total of {0:d} {1:s} worlds extracted on the Flash version.".format(0, note))
            hasworld = False
    return data

data = extractworld("", 0, "Re")
data = extractworld(data, 1200, "Dw")

f = open("CCS_Flash_configs.json", "w")
f.write("[" + data.rstrip(",") + "]")
f.close()
