import numpy as np
import pandas as pd
import plotHelper as ph
import pendulum as pend
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import style
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import MultipleLocator

style.use('Solarize_Light2')

MRKOPEN = "09:30:00"
MRKCLOSE = "16:15:00"
GLOBEX = "20:00:00"
DATEFORMAT = "dd-MM/DD HH:mm"

if __name__ == "__main__": 
    ''' Read and format data'''
    data = pd.read_csv('ES0619.csv', sep=";")
    data.columns = ["DateTime","Open","High","Low","Close","Volume"]
    data["DateTime"] = data["DateTime"].apply(lambda x: pend.parse(x))
    data = data.values.tolist()
    for row in data:
        row[0] = pend.instance(row[0])
    
    '''partition data into sunday->saturday chunks
        skip first week due to weird start time
    '''
    partition = []
    temp = []
    sundayFlag = None 
    for each in data:
        day = each[0].day_of_week
        #skip the fist sunday
        if sundayFlag == None:
            if day == 0:
                continue
            else:
                sundayFlag = False 
        #start with second sunday
        if day == 0 and sundayFlag == False:
            partition.append(temp[:])
            temp.clear()
            temp.append(each)
            sundayFlag = True
        elif day == 0 and sundayFlag == True:
            temp.append(each)
        else:
            temp.append(each)
            sundayFlag = False
    partition.pop(0)#first element contains data from the first week, need to be removed
    
    ''' Generate plot for each week partition'''
    for each in partition:
        fig = ph.basicStockChart(each,MRKOPEN,MRKCLOSE,DATEFORMAT=DATEFORMAT)
        
        '''
        Here we are looking for key points, to draw our support and resistance        
        '''
        keypts = []
        missingFlag = True
        for x in each:
            if x[0].to_time_string() == GLOBEX or x[0].to_time_string() == MRKOPEN:
                keypts.append(x)
                missingFlag = False
            elif x[0].diff(pend.parse(x[0].to_date_string()+" "+GLOBEX),False).in_minutes() == -1 and missingFlag:
                keypts.append(x)
                missingFlag = True
            elif x[0].diff(pend.parse(x[0].to_date_string()+" "+MRKOPEN),False).in_minutes() == -1 and missingFlag:
                keypts.append(x)
                missingFalg = True
        
        keyDate = np.array([x[0] for x in keypts])
        keyTime = np.array([x[0].to_time_string() for x in keypts])
        keyPrice = np.array([x[1] for x in keypts])
        #plots globex and market open
        for i in range(len(keyPrice)):
            if keyTime[i] == GLOBEX:
                plt.hlines(y=keyPrice[i],xmin=keyDate[i].format(DATEFORMAT),
                        xmax = keyDate[i].add(days=1).format(DATEFORMAT),linewidth = 0.5,color="r",linestyle="-")
            else:
                plt.hlines(y=keyPrice[i],xmin=keyDate[i].format(DATEFORMAT),
                        xmax = keyDate[i].add(days=1).format(DATEFORMAT),linewidth = 0.5,color="b",linestyle="-")

        ax = plt.axes()
        ax.xaxis.set_major_locator(MultipleLocator(100))
        plt.xticks(rotation=90)
        plt.margins(x=0.005)
        plt.tight_layout()
        plt.subplots_adjust(0.031,0.135,0.992,0.985)
        plt.show()
