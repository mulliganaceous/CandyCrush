import os as K
import re as R

# Input tweak information.
# If folder is not found, a traceback is generated.
tweak = input("Enter tweak folder: ")
path = K.getcwd() + '/' + tweak
print(path)

# Generate gallery file
source = "<gallery widths=96px spacing=small columns=8 hideaddbutton=true>\n"
for filename in K.listdir(path):
    matcher = R.match(r"E(\d*)-(\d*)@([E,P,U]).*", filename)
    if (matcher):
        ep = int(matcher.group(1))
        lvl = int(matcher.group(2))
        def L(ep, lvl):
            if ep < 3:
                return 10*(ep - 1) + lvl
            return 15*(ep - 1) + lvl - 10
        img, name, total = None, None, L(ep, lvl)
        if matcher.group(3) == 'E':
            img = "{0:s}".format(filename)
            name = "[[Level {0:d}|E{1:d}-{2:d}]]".format(total, ep, lvl)
        elif matcher.group(3) == 'P':
            img = "{0:s}".format(filename)
            name = "[[Level {0:d}/Versions|''Past'']]".format(total)
        source += "{0:s}|{1:s}\n".format(img, name)
source += "</gallery>"
f = open(path + '/' + tweak + "gallery.txt", 'w')
f.write(source)
f.close()
