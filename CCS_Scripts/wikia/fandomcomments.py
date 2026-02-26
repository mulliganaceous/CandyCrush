import urllib.request
from urllib.error import HTTPError
import json
from datetime import datetime

MAXLVL = 21605

# Determine URL
def extract_all():
    """No longer feasible. Requires a bot account."""
    PREFIX = "https://candycrush.fandom.com/wikia.php?controller=ArticleCommentsController&method=getComments"
    for lvl in range(1,MAXLVL + 1):
        TITLE = "&title=Level+{0:d}".format(lvl)
        NAMESPACE = "&namespace=0"
        url = "{0:s}{1:s}{2:s}".format(PREFIX, TITLE, NAMESPACE)
        file = None
        try:
            with urllib.request.urlopen(url) as response:
                file = response.read()
                g = open('comments_L{0:05d}.json'.format(lvl), 'wb')
                g.write(file)
                g.close()
            print('L{0:5d} {1:d}'.format(lvl, len(file)))
        except HTTPError as e:
            print(e)

def obtain_json(lvl):
    # Extract json
    g = open('comments_L{0:05d}.json'.format(lvl), 'r')
    r = g.read()
    j = json.loads(r)
    g.close()
    return j, len(r)

# Auxiliary function
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

extract_all()
