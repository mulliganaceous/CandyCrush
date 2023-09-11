import json
j = json.load(open("configs_flash.json"))
count, level = 0, 0
for u in j:
    level += 1
    if (u["gameData"]["gameModeName"] == "Classic moves"):
        print("#{3:d}\tL{4:d}\t({0:3d}-{1:2d})\t{2:s}".format(u["episode"], u["level"], u["gameData"]["gameModeName"], count, level))
        count += 1
