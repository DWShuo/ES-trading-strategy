import numpy as np
import pendulum as pend
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator

def surfacePlot(zlabel,x,y,z):
    #Use set property to remove duplicate in x & y
    xSet = list(set(x))
    ySet = list(set(y))
    xSet.sort()
    ySet.sort()
    #enumerate x and y label since pyplot cant take strings as ticks
    xEnum = [[j,i] for i,j in enumerate(xSet)]
    yEnum = [[j,i] for i,j in enumerate(ySet)]
    #create map so we can go back and replace enumeration with date-time label
    xDict = {xEnum[i][0]: xEnum[i][1] for i in range(0,len(xEnum))}
    yDict = {yEnum[i][0]: yEnum[i][1] for i in range(0,len(yEnum))}
    xNumeric = [xDict[a] for a in x]
    yNumeric = [yDict[a] for a in y]
    ax = plt.axes(projection='3d')
    ax.plot_trisurf(xNumeric, yNumeric, z, cmap=cm.jet, linewidth=0.1)
    ax.set_xlabel('Date')
    ax.set_ylabel('Time')
    ax.set_zlabel(zlabel)
    ax.xaxis.set_major_locator(MultipleLocator(5))#set how many ticks we want
    #replace enumerated axis labels with date and time labels  
    ax.set_xticklabels([xSet[0],xSet[0],xSet[5],xSet[10],xSet[15],xSet[20],xSet[25],xSet[30],xSet[35],xSet[40],xSet[45],xSet[50],xSet[55],xSet[60],xSet[65],xSet[70],xSet[75],xSet[80],xSet[40],xSet[40],xSet[95]])
    ax.set_yticklabels([ySet[0],ySet[0],ySet[200],ySet[400],ySet[600],ySet[800],ySet[1000],ySet[1200],ySet[1400],ySet[390]])
    plt.xticks(rotation=45)
    plt.show()

def basicStockChart(data,start,end,DATEFORMAT="MM-DD-YY HH:mm",DEBUG=False):
    fig = plt.figure()
    date = np.array([x[0] for x in data])
    pOpen = np.array([x[1] for x in data])
    plt.plot([x.format(DATEFORMAT) for x in date],pOpen,color="black",linewidth=0.5)
    #find open and close index locations
    openClose = []
    missingFlag = True
    for x in data:
        if x[0].to_time_string() == start or x[0].to_time_string() == end:
            openClose.append(x)
            missingFlag = False
        elif x[0].diff(pend.parse(x[0].to_date_string()+" "+start),False).in_minutes() == -1 and missingFlag:
            openClose.append(x)
            missingFlag = True
        elif x[0].diff(pend.parse(x[0].to_date_string()+" "+end),False).in_minutes() == -1 and missingFlag:
            openClose.append(x)
            missingFalg = True
    #set background to grey
    plt.axvspan(date[0].format(DATEFORMAT),date[-1].format(DATEFORMAT),facecolor="grey",alpha=0.25)
    #set market open and close time span to white
    for i in range(0,len(openClose),2):
        if DEBUG == True:
            print(openClose[i][0].format(DATEFORMAT),openClose[i+1][0].format(DATEFORMAT))
        plt.axvspan(openClose[i][0].format(DATEFORMAT),openClose[i+1][0].format(DATEFORMAT)
                ,facecolor="white",alpha=0.85)
    return fig
