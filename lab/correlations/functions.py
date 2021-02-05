import json
import sys
import os


def is_short(n):
    blacklist = ['Short', 'Inverse', 'Bear', 'Decline', 'Tail']
    for b in blacklist:
        if (b in n):
            return True
    return False