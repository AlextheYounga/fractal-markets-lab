import sys
from .tweet import tweet_confirm 

def tweet_test():
    

    while True:
        sys.stdout.write('Write tweet:')
        tweet = input()        
        while True:
            answer = str(input('Run again? (y/n): '))
            if answer in ('y', 'n'):
                break
            print("invalid input.")
        if answer == 'y':
            continue
        else:
            print("Tweet Sent")
            break
