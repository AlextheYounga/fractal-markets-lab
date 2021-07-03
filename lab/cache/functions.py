import os
import json
import sys
import re


def pathfinder(path, key):
    separators = ['-', '.', '_', ':', '->']
    for sep in separators:
        if (sep in key):
            levels = key.split(sep)

            for level in levels:
                path = path + f"/{level}"
                if not os.path.exists(path):
                    os.mkdir(path)
            break

    path = path + f"/{path.split('/')[-1]}.txt"

    return path


def readTxtFile(path):
    print(path)
    txtfile = open(path, "r")
    print(re.search(r"\[([A-Za-z0-9_]+)\]", txtfile.readlines()[0]))
    sys.exit()
    # TODO: Figure out how tofind type.
    fmt = re.search(r"\[([A-Za-z0-9_]+)\]", txtfile.readlines()[0]).group(1)

    if (fmt == "<class 'list'>"):
        items = []
        for line in txtfile:
            stripped_line = line.strip()
            line_list = stripped_line.split()
            items.append(str(line_list[0]))
        txtfile.close()

        return list(dict.fromkeys(items))

    if (fmt == "<class 'str'>"):
        return str(txtfile)

    if (fmt == "<class 'dict'>"):
        return json.loads(txtfile)


def writeTxtFile(data, path, append=False):
    # Appending function
    if (append):
        checked = readTxtFile(path)
        if (checked):
            lst = list(dict.fromkeys(checked + data))

    fmt = type(data)
    txtfile = path
    # os.remove(txtfile)
    with open(txtfile, 'w') as f:
        f.write("%s\n" % f"{fmt}")
        if (fmt == list):
            for item in lst:
                f.write("%s\n" % item)
        if (fmt == str):
            f.write(data)
        if (fmt == dict):
            f.write(json.dumps(data))
            
    return True


def deleteFromTxTFile(lst, path):
    read = readTxtFile(path)
    for l in lst:
        read.remove(l)

    os.remove(path)
    with open(path, 'w') as f:
        for item in read:
            f.write("%s\n" % item)
