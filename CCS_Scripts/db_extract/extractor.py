import sqlite3
import json
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=65536)

con = sqlite3.connect("levels_batched.db")
cur = con.cursor()
res = cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
arr = res.fetchall()

TABLENAME = "batched_levels"
res = cur.execute("SELECT * FROM {0:s}".format(TABLENAME))
arr = res.fetchall()

def obtain_attribute(n, a, fallback):
    try:
        return json.loads(n)[a]
    except KeyError:
        return fallback

def enumerate_moves():
    a = list(map(lambda lvl: json.loads(lvl[1])['moveLimit'], arr))
    fig, ax = plt.subplots(figsize=(40, 10))
    ax.set_xticks(ticks=range(0, 25000, 1000), minor=True)
    ax.set_xticks(range(0, 25000, 5000))
    ax.grid(which='both')
    ax.plot(range(1, len(a) + 1), a, 'x', markeredgewidth=1, alpha=0.25)

    plt.savefig("moveLimit.png", bbox_inches='tight')
    plt.show()

    fig, ax = plt.subplots(figsize=(20, 10))
    ax.grid(which='both')
    values, bins, bars = ax.hist(a, bins=range(10, 51, 1), align='left')
    ax.bar_label(bars)

    plt.savefig("moveLimitHist1.png", bbox_inches='tight')
    plt.show()

def enumerate_board_sizes():
    rows = list(map(lambda lvl: obtain_attribute(lvl[1], 'boardRows', -1), arr))
    cols = list(map(lambda lvl: obtain_attribute(lvl[1], 'boardCols', -1), arr))
    unusually_sized = np.astype(np.column_stack([range(1, len(rows) + 1), rows, cols]), np.int32)
    np.savetxt("board-sizes.tsv", unusually_sized, fmt='%d', delimiter='\t')

ORDERNAMES = [
    "NULL",
    "Red",
    "Blue",
    "Yellow",
    "Orange",
    "Purple",
    "Green",
    "Wrapped",
    "Striped",
    "Color Bomb",
    "S+S",
    "S+W",
    "S+C",
    "C+C",
    "W+C",
    "W+W",
    "Chocolate",
    "Frosting",
    "Liquorice Shell",
    "Liquorice Swirl",
    "Candy Bomb",
    "Jelly Fish",
    "Cake Bomb",
    "Mystery Candy",
    "Magic Mixer",
    "Toffee Swirl",
    "Dark Chocolate",
    "Candy Cane Curl",
    "Rainbow Twist",
    "Candy Frog",
    "Sugar Coat",
    "Bubblegum Pop",
    "Licorice Curl",
    "Sour Skull",
    "Bonbon Blitz",
    "Jelly Jar",
    "Candy Cobra",
    "Wonderful Wrapper",
    "Gumball",
    "Mall-O-Matic",
    "Citrus Chew",
    "Colour Cluster",
    "",
]

def enumerate_orders():
    enumerated_total = {}

    enumerated_goals = {}
    orders = list(map(lambda lvl: obtain_attribute(lvl[1], '_itemsToOrder', []), arr))
    maxindex = 0
    for k in range(len(orders)):
        orderlist = orders[k]
        lvl = k + 1
        for item in orderlist:
            itemtype = item["item"]
            if itemtype > maxindex:
                maxindex = itemtype
            if itemtype not in enumerated_goals:
                enumerated_goals[itemtype] = set()
            enumerated_goals[itemtype] |= {lvl}
    for itemtype in range(1, maxindex):
        if itemtype not in enumerated_goals:
            enumerated_goals[itemtype] = set()
        enumerated_total[itemtype] = enumerated_goals[itemtype]

    enumerated_orderlocks = {}
    orders = orders = list(map(lambda lvl: obtain_attribute(lvl[1], 'orlocks', None), arr))
    for k in range(len(orders)):
        orderlist = orders[k]
        if not orderlist:
            continue
        lvl = k + 1
        for item in orderlist:
            if 'data' in item:
                itemtype = item['data'][4]
            else:
                itemtype = item[4]
            if itemtype > maxindex:
                maxindex = itemtype
            if itemtype not in enumerated_orderlocks:
                enumerated_orderlocks[itemtype] = set()
            enumerated_orderlocks[itemtype] |= {lvl}
    for itemtype in range(1, maxindex + 1):
        if itemtype not in enumerated_orderlocks:
            enumerated_orderlocks[itemtype] = set()
        enumerated_total[itemtype] = enumerated_goals[itemtype] | enumerated_orderlocks[itemtype]

    return enumerated_goals, enumerated_orderlocks, enumerated_total

def enumerate_board_elements():
    boards = list(map(lambda lvl: obtain_attribute(lvl[1], 'tileMap', []), arr))
    enumerated = {}
    for k in range(len(boards)):
        lvl = k + 1
        for row in boards[k]:
            for tile in row:
                if len(tile) % 3 != 0:
                    raise Exception()
                for c in range(0, len(tile), 3):
                    telement = tile[c:c+3]
                    if telement not in enumerated:
                        enumerated[telement] = set()
                    enumerated[telement] |= {lvl}
    return enumerated

def enumerate_magic_mixer():
    amount = list(map(lambda lvl: obtain_attribute(lvl[1], 'evilSpawnerAmount', -1), arr))
    elements = list(map(lambda lvl: obtain_attribute(lvl[1], 'evilSpawnerElements', []), arr))
    interval = list(map(lambda lvl: obtain_attribute(lvl[1], 'evilSpawnerInterval', -1), arr))
    return list(zip(amount, elements, interval))

def enumerate_bombspawn():
    turns = list(map(lambda lvl: obtain_attribute(lvl[1], "pepperCandyExplosionTurns", -1), arr))
    amount = list(map(lambda lvl: obtain_attribute(lvl[1], 'pepperCandyMax', -1), arr))
    spawn = list(map(lambda lvl: obtain_attribute(lvl[1], 'pepperCandySpawn', -1), arr))
    return list(zip(turns, amount, spawn))

def count_board_elements_in_level(id, lvl, arr):
    board = json.loads(arr[lvl][1])['tileMap']
    count = 0
    for row in board:
        for tile in row:
            if len(tile) % 3 != 0:
                raise Exception()
            for c in range(0, len(tile), 3):
                telement = int(tile[c:c+3])
                count += (telement == id)
    return count

def count_board_elements_across_levels(id, arr):
    levels = {}
    for lvl in arr:
        board = json.loads(lvl[1])['tileMap']
        count = 0
        for row in board:
            for tile in row:
                if len(tile) % 3 != 0:
                    raise Exception()
                for c in range(0, len(tile), 3):
                    telement = int(tile[c:c+3])
                    count += (telement == id)
        if count > 0:
            levels[lvl[0] + 1] = count
    return levels

def _demo1():
    print(list(map(lambda lvl: obtain_attribute(lvl[1], 'orlocks', None), arr)))
    orders, orderlocks, allorders = enumerate_orders()
    keys = sorted(orders.keys())
    for itemtype in keys:
        print("{0:d}\t{1:d}\t{2:d}\t{3:d}".format(itemtype, len(orders[itemtype]), len(orderlocks[itemtype]), len(allorders[itemtype])))

    for itemtype in range(10, 16):
        print("{0:d}\t\{1:s}\t{2:s}\t\{3:s}".format(itemtype, str(orders[itemtype]), str(orderlocks[itemtype]), str(allorders[itemtype])))

def _demo2():
    boards = enumerate_board_elements()
    keys = sorted(boards.keys())
    for k in keys:
        if (len(boards[k]) > 16):
            print("{0:s}\t{1:d}".format(k, len(boards[k])))
        else:
            print("{0:s}\t{1:s}".format(k, str(boards[k])))

def _demo3():
    mixers = enumerate_magic_mixer()
    for k in range(len(mixers)):
        count = count_board_elements_in_level(62, k, arr)
        if mixers[k][1] or count:
            if 1 in mixers[k][1]:
                print(k + 1, mixers[k], count)

def _demo4():
    bombspawn = enumerate_bombspawn()
    for k in range(len(bombspawn)):
        if bombspawn[k][1] >= 0 or bombspawn[k][2] >= 0:
            print(k + 1, bombspawn[k])

res = count_board_elements_across_levels(7, arr)
for k in res:
    print(k, res[k])

res = cur.execute("SELECT * FROM batched_levels WHERE rowid=4045;")
lvl = res.fetchone()
lvl = json.loads(lvl[1])['tileMap']
g = open("tilemap.tsv", 'w')
for row in lvl:
    for tile in row:
        g.write(tile + "\t")
    g.write("\n")