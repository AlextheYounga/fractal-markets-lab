import json
import csv
import os
from os import path
import pandas
from pandas import read_csv
import datetime
from ..definitions import STORAGE


def parsePortfolioCSV(fullpath):
    """
    Parameters
    ----------
    path     : string
               complete file path

    Returns
    -------
    dict
        CSV values converted to dict
    """

    with open(fullpath, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        print(reader)
    # portfolio = {}
    # reader = pandas.read_csv(fullpath, skiprows=8)[:-1].to_dict()
    # print(reader)


    # return portfolio
    return


def latestFile(files):
    """
    Parameters
    ----------
    files    : list
               list of filenames

    Returns
    -------
    string
        Complete path of last modified file
    """
    ctimes = {}
    for f in files:
        path = "{}/portfolio/{}".format(STORAGE, f)
        ctime = os.path.getmtime(path)
        ctimes[ctime] = path

    return ctimes.pop(max(ctimes))
