from dotenv import load_dotenv
import json
import sys
from .methodology import calculate
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import pylab
import numpy as np
load_dotenv()



# def run(update=False):
#     index = calculate(update)


# TODO Fix Matplotlib
def graph(update=False):
    index = calculate(update)

    x = index.keys()
    y = index.values()

    fig = plt.subplots(figsize=(12, 7))

    plt.plot(x, y, label='Index Value')
    plt.xlabel('x Date')
    plt.ylabel('y Value')
    plt.title("Inflation Index")
    plt.xticks(np.arange(0, len(x)+1, 126))
    plt.xticks(rotation=45)

    # plt.show()
    plt.draw()
    plt.pause(1)
    input("<Hit Enter To Close>")
    plt.close()
