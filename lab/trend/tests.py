import sys
from ..core.functions import prompt_yes_no


a = [1, 2, 3, 4, 5, 6, 7, 8, 9]
for i in a:
    if (i == 4):
        confirm = prompt_yes_no('continue?')
        if (confirm):
            print(i)