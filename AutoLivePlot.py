import os
import argparse
import math
import questionary
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import warnings
warnings.filterwarnings("ignore")

VERSION = 1.0

CSVs = []
Lines = []
AXS = []
PlotName = ''
SaveDir = os.getcwd() + "/measurements"
colours = ['mediumblue', 'orange', 'yellowgreen', 'tomato', 
           'orchid', 'violet', 'olive', 'cyan']

plt.rcParams["savefig.directory"] = SaveDir

def main(args):
    global PlotName
    global CSVs
    global Lines
    global AXS
    global SaveDir

    if not os.path.exists(SaveDir):
        os.makedirs(SaveDir)

    PlotName = args.name
    CSVs = args.csvs
    dateTimeCol, DFS = prepareDataframe(args.csvs)
    numCols = DFS.shape[1]
    s = plotSize(numCols)

    fig, AXS = plt.subplots(s, s, sharex=True)
    fig.suptitle(PlotName)
    
    i=0
    for col in DFS.columns.values:
        colour = colours[i % len(colours)]
        line, = AXS.flat[i].plot([], [], color=colour)
        AXS.flat[i].set_title(col)
        Lines.append(line)
        i += 1
    
    for ax in AXS[s-1].flat:
        ax.set(xlabel=args.xlabel)

    try:
        ani = FuncAnimation(fig, animate, interval=200, cache_frame_data=False)

        plt.show()
    except KeyboardInterrupt:
        plt.savefig(SaveDir + '/' + PlotName)
        exit(0)

def prepareDataframe(csvs:list):
    allDFS = pd.DataFrame()
    dateTimeCol = pd.DataFrame()
    for csv in csvs:
        df = pd.read_csv(csv)
        dateTimeCol = df.select_dtypes(include=['object'])
        df = df.select_dtypes(exclude=['object'])
        allDFS = pd.concat([allDFS, df], axis=1)
    allDFS.dropna(inplace=True)
    allDFS = allDFS.head(dateTimeCol.shape[0])
    dateTimeCol = dateTimeCol.head(allDFS.shape[0])
    return dateTimeCol, allDFS.dropna()

def plotSize(c:int):
    return math.ceil(math.sqrt(c))

def getBufferPrecision(decimal):
    return str(decimal)[::-1].find('.')

def animate(frame):
    global CSVs
    global Lines
    global AXS
    global PlotName
    global SaveDir

    dateTimeCol, df = prepareDataframe(CSVs)

    dateName = dateTimeCol.columns.values[0]
    dateTimeCol[dateName] = pd.to_datetime(dateTimeCol[dateName])
    dateTimeCol[dateName] = dateTimeCol[dateName] - dateTimeCol[dateName][0]
    dateTimeCol[dateName] = dateTimeCol[dateName].dt.total_seconds()
    t = np.asarray(dateTimeCol[dateName], int)

    i = 0
    for colName, colData in df.items():
        b = getBufferPrecision(colData.mean())
        if b > 0:
            buf = 1 / (b*10)
        else:
            buf = 1
        Lines[i].set_data(t, colData)
        AXS.flat[i].set_ylim([colData.min() - buf, colData.max() + buf])
        i += 1
    
    for ax in AXS.flat:
        ax.set_xlim([0, max(t)])
    plt.savefig(SaveDir + '/' + PlotName)




if __name__ == '__main__':
    questionary.print('************************************************'.center(50))
    questionary.print('Auto Live Plot'.center(50), style='bold')
    questionary.print(f'Version {VERSION}'.center(50), style='italic')
    questionary.print('Written by Maria Buckley'.center(50), style='italic')
    questionary.print('************************************************'.center(50))

    parser = argparse.ArgumentParser(description='set user arguments')
    parser.add_argument('-n', '--name', help='Name to save plot under', default='Auto Live Plot')
    parser.add_argument('-x', '--xlabel', help='X axis label', default='Time(s)')
    parser.add_argument('-c', '--csvs', nargs='+', help='<Required> Path to the csvs to plot', required=True)
    
    main(parser.parse_args())