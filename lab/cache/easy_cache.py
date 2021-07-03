import json
from colored import stylize
from ..core.functions import zipfolder
from .functions import *
import cryptography
import sys
import os
import colored


class EasyCache:
    # My own storage system because this is just how I am.
    def __init__(self):
        self.path = 'lab/cache/ez'  # better for complex data
        self.easy_path = 'lab/cache/ez/ez.json'  # for simple data

    def get(key):
        path = pathfinder(EasyCache().path, key)
        if os.path.exists(path):
            return readTxtFile(path)

        with open(path) as jsonfile:
            cache = json.loads(jsonfile.read())

        jsonfile.close()
        return cache.get(key, False)

    def put(key, value, method='easy'):

        if (method == 'easy'):
            path = EasyCache().path
            with open(path) as jsonfile:
                cache = json.loads(jsonfile.read())
            jsonfile.close()

            cache[key] = value

            with open(path, 'w') as jsonfile:
                json.dump(cache, jsonfile)
            jsonfile.close()

            return True

        if (method == 'complex'):
            path = pathfinder(EasyCache().path, key)
            # print(path)
            # sys.exit()
            writeTxtFile(value, path)
            return True

    def clear():
        ez = EasyCache()
        os.remove(ez.path)
        os.mkdir(ez.path)
        with open(ez.easy_path, 'w') as jsonfile:
            json.dump({}, jsonfile)
        jsonfile.close()

        print(stylize('Cache cleared!', colored.fg('green')))
