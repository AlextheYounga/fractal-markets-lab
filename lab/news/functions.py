import django
from django.apps import apps
import sys
import json
import os
import re
django.setup()


def clean_tickers(tickers):
    Stock = apps.get_model('database', 'Stock')
    db_tickers = Stock.objects.all().values_list('ticker', flat=True)
    cleaned = []

    def checkLowerCase(t):
        for c in t:  # Checking for lowercase letters
            if (c.islower()):
                return True
        return False

    for t in tickers:
        if(' ' not in t):
            if ('.' not in t):
                if (t != ''):
                    if (checkLowerCase(t) == False):
                        if (t in db_tickers):
                            if (':' in t):
                                t = t.split(':')[1]
                            if (t not in cleaned):
                                cleaned.append(t)

    return cleaned


def blacklistWords():
    txtfile = open("lab/news/blacklist_words.txt", "r")

    blacklist = []
    for line in txtfile:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        blacklist.append(str(line_list[0]))

    txtfile.close()

    return list(dict.fromkeys(blacklist))


def blacklistUrls():
    txtfile = open("lab/news/blacklist_urls.txt", "r")

    blacklist = []
    for line in txtfile:
        stripped_line = line.strip()
        line_list = stripped_line.split()
        blacklist.append(str(line_list[0]))

    txtfile.close()

    return list(dict.fromkeys(blacklist))


def updateBlacklist(lst):
    txtfile = "lab/news/blacklist_words.txt"
    os.remove(txtfile)
    with open(txtfile, 'w') as f:
        for item in lst:
            f.write("%s\n" % item)


def removeBadCharacters(word):
    if (isinstance(word, list)):
        word = str(word[0])

    regex = re.compile('[^A-Z]')
    word = regex.sub('', word)

    if (len(word) > 5):
        return False

    if any(c for c in word if c.islower()):
        return False

    return word