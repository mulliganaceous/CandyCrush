import urllib.request
from urllib.error import HTTPError
import json
import numpy as np
from datetime import datetime

# Determine timestamp and version
print("Enter timestamp: ")
timestamp = int(input())
print("Enter u-code: ")
variation = int(input())

# Determine URL
PREFIX = 'https://king-candycrush-prod.secure2.footprint.net/wfp'
url = '{}/hl-v2.json?v={}'.format(PREFIX, timestamp)
file = None
try:
    with urllib.request.urlopen(url) as response:
        file = response.read()
        g = open('hl-v2-{}.json'.format(timestamp), 'wb')
        g.write(file)
        g.close()
except HTTPError:
    print('404 error')
    exit(1)

# Generate hexagon list
jsonload = json.loads(file)['hardlevels']
hexagonstring = ['', 'Hexagon', 'Super Hard', 'Owl']

def generate_hexagonlist(hexversion=[variation]):
    hexagons = {}
    maxkey = 0
    maxrating = 0
    for hl in jsonload:
        if hl['u'] in hexversion:
            if not hl['e'] in hexagons:
                hexagons[hl['e']] = {hl['l']: hl}
                if maxrating < hl['d']:
                    maxrating = hl['d']
            else:
                hexagons[hl['e']][hl['l']] = hl
    print("Length of dataset: {}".format(len(hexagons)))
    print("Highest classification: {}".format(maxrating))
    return hexagons, len(hexagons) + 1, maxrating

def _totallevel(e:int, l:int):
    if l == -1:
        if e <= 2:
            return 10
        else:
            return 15
    if e <= 2:
        return 10*(e-1) + l
    else:
        return 15*(e-1) - 10 + l

def _hexagonality(hexagons, e:int, l:int):
    if e in hexagons and l in hexagons[e]:
        return hexagons[e][l]['d']
    else:
        return 0

def _hexagonstring(hexagons, e:int, l:int):
    hexagonality = _hexagonality(hexagons, e, l)
    if hexagonality < len(hexagonstring):
        return hexagonstring[hexagonality]
    else:
        return "Legendary"

hexagons, maxkey, maxrating = generate_hexagonlist()

# Convert hexagon list to Lua file
def output_lualist(hexagons):
    g = open('hl-v2-{}-{}.lua'.format(timestamp, variation), 'w')

    # Print out to file
    g.write("-- Instructions: The number in brackets indicate corresponding level.\n" + \
            "-- change '' to 'Hexagon' or 'Super Hard' or 'Owl' to assign rating\n" + \
            "-- An empty string indicates that this level is not a hexagon.\n" + \
            "-- Hexagon level last updated @ {0:s}\n\n".format(datetime.utcfromtimestamp(timestamp/1000).isoformat()) + \
            "return {\n")
    
    for e in range(1,maxkey):
        if e in hexagons:
            g.write("\t--Episode {0:d} ({1:d})\n".format(e, len(hexagons[e])))
        else:
            g.write("\t--Episode {0:d} (0)\n".format(e))
        for l in range(1,_totallevel(e,-1)+1):
            g.write("\t[{0:d}] = \'{1:s}\',".format(_totallevel(e,l), _hexagonstring(hexagons,e,l)))
            g.write("\n")
    g.write("}\n-- Lua code written by Catinthedark and Wildoneshelper.\n" + \
            "-- Automatic extraction methods devised by Mulliganaceous (a mulligan)")
    g.close()
    
output_lualist(hexagons)

# Use NumPy data to print as data
hexcount = np.zeros((maxkey, maxrating))
hexcount.dtype = np.longlong
for k in range(1,len(hexagons)):
    if k in hexagons:
        print('E{0:3d} ({1:d})'.format(k, len(hexagons[k])))
        for l in hexagons[k]:
            hl = hexagons[k][l]
            print('\tv{0:d} L{1:5d} {2:s} '.format(hl['u'], _totallevel(hl['e'], hl['l']), '*'*hl['d']))
            hexcount[k,hl['d']-1] += 1
    else:
        print('E{0:3d} (0)'.format(k))
        print('\tEMPTY')

for k in range(1,maxkey):
    print("E{0:3d}\t{1:d}\t{2:s}".format(k, np.sum(hexcount[k]), str(hexcount[k])))
