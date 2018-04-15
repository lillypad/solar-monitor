# Import the necessary modules
import time
time_0 = time.time()
import datetime as dt
import os
#import sqlite3
from sqlite3 import connect as ConnectSQLite
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib import style
time_1 = time.time()
print ("imports done with time: %s" % (time_1 - time_0))

style.use('seaborn-whitegrid')
print ("style set")

# initialize variables and 1st run assignments.
dbpath = "/media/pi/SOLARUSB/SolarMonitor/"
dbfile = "SolarDataCollection.db"

# Define the datatype [list] for the plot
x1 = []
y11 = []
y12 = []
y21 = []
y22 = []

# Connect to database file
DBconnect = ConnectSQLite(dbpath + dbfile)
DBcursor = DBconnect.cursor()

# Get and plot data function
def GetDataAndPlot(SD, ED, DP11, DP21 = 'Null', DP12 = 'Null', DP22 = 'Null'):
    # Setup size of figure
    fig = plt.figure(figsize=(14,9))

    # Retrive data from the database and load into lists to plot
    # If the first datapoint of the 2nd subplot is not null then create 2 subplots 
    if DP21 != 'Null':
        ax2 = plt.subplot2grid((2,1),(1,0), rowspan=1, colspan=1)
        ax1 = plt.subplot2grid((2,1),(0,0), rowspan=1, colspan=1)
        
        # Add the 2nd y axis on the subplots if not null
        if DP12 != 'Null':
            ax1v = ax1.twinx()
        if DP22 != 'Null':
            ax2v = ax2.twinx()

        # Add Plot title(fixed for now. will fix later)
        ax1.set_title('RV Solar Data',fontsize='20', color='purple')

        # query the database and process 1 datapoint on each of the 2 subplots
        if DP12 == 'Null' and DP22 == 'Null':
            DBcursor.execute("SELECT [Date Time], [%s], [%s] FROM [Raw Solar Data] WHERE [Date Time] >= ? AND [Date Time] <= ?" % (DP11, DP21), (SD,ED))
            for row in DBcursor.fetchall():
                x1.append(mdates.datestr2num(row[0]))
                y11.append(row[1])
                y21.append(row[2])
            for label in ax2.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(True)

            for label in ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(False)
            plt.subplots_adjust(left=0.1, bottom=0.12, right=0.94, top=0.94, wspace=0.2, hspace=0.07)

        # query the database and process 2 datapoints on 1st subplot & 1 datapoint on the 2nd subplot
        if DP12 != 'Null' and DP22 == 'Null':
            DBcursor.execute("SELECT [Date Time], [%s], [%s], [%s] FROM [Raw Solar Data] WHERE [Date Time] >= ? AND [Date Time] <= ?" % (DP11, DP21, DP12), (SD,ED))
            for row in DBcursor.fetchall():
                x1.append(mdates.datestr2num(row[0]))
                y11.append(row[1])
                y21.append(row[2])
                y12.append(row[3])
            for label in ax2.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(True)

            for label in ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(False)
            plt.subplots_adjust(left=0.1, bottom=0.12, right=0.9, top=0.94, wspace=0.2, hspace=0.07)
            ax1v.set_prop_cycle('color', ['red', 'blue'])
            ax1v.yaxis.label.set_color('r')
            ax1v.plot_date(x1,y12, '-', label=DP12)
            ax1v.set_ylabel(DP12)
            ax1v.minorticks_on()

        # query the database and process 1 datapoint on 1st subplot & 2 datapoints on the 2nd subplot
        if DP12 == 'Null' and DP22 != 'Null':
            DBcursor.execute("SELECT [Date Time], [%s], [%s], [%s] FROM [Raw Solar Data] WHERE [Date Time] >= ? AND [Date Time] <= ?" % (DP11, DP21, DP22), (SD,ED))
            for row in DBcursor.fetchall():
                x1.append(mdates.datestr2num(row[0]))
                y11.append(row[1])
                y21.append(row[2])
                y22.append(row[3])
            for label in ax2.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(True)

            for label in ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(False)
            plt.subplots_adjust(left=0.1, bottom=0.12, right=0.9, top=0.94, wspace=0.2, hspace=0.07)
            ax2v.set_prop_cycle('color', ['red', 'blue'])
            ax2v.yaxis.label.set_color('r')
            ax2v.plot_date(x1,y22, '-', label=DP22)
            ax2v.set_ylabel(DP22)
            ax2v.minorticks_on()

        # query the database and process 2 datapoints on 1st subplot & 2 datapoints on the 2nd subplot
        if DP12 != 'Null' and DP22 != 'Null':
            print ("query database for data")
            DBcursor.execute("SELECT [Date Time], [%s], [%s], [%s], [%s] FROM [Raw Solar Data] WHERE [Date Time] >= ? AND [Date Time] <= ?" % (DP11, DP21, DP12, DP22), (SD,ED))
            print ("get database data done")
            for row in DBcursor.fetchall():
                x1.append(mdates.datestr2num(row[0]))
                y11.append(row[1])
                y21.append(row[2])
                y12.append(row[3])
                y22.append(row[4])
            for label in ax2.xaxis.get_ticklabels():
                label.set_color('black')
                label.set_fontsize(16)
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(True)

            for label in ax1.xaxis.get_ticklabels():
                label.set_visible(False)
            ax1v.set_prop_cycle('color', ['red', 'blue'])
            ax2v.set_prop_cycle('color', ['red', 'blue'])
            ax1v.yaxis.label.set_color('r')
            ax1v.yaxis.label.set_fontsize(16)
            ax2v.yaxis.label.set_color('r')
            ax2v.yaxis.label.set_fontsize(16)
            ax1v.plot_date(x1,y12, '-', label=DP12)
            ax2v.plot_date(x1,y22, '-', label=DP22)
            ax1v.grid(True, linestyle='-')
            ax2v.grid(True, linestyle='-')            
            ax1v.set_ylabel(DP12)
            ax2v.set_ylabel(DP22)

        xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
        ax1.xaxis.set_major_formatter(xfmt)
        ax2.xaxis.set_major_formatter(xfmt)
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(15))
        ax2.xaxis.set_major_locator(mticker.MaxNLocator(15))
        
        ax1.set_prop_cycle('color', ['blue', 'red'])
        ax2.set_prop_cycle('color', ['blue', 'red'])
        
        ax1.plot_date(x1,y11, '-', label=DP11)
        ax2.plot_date(x1,y21, '-', label=DP21)
        
        ax1.grid(True, linestyle='-')
        ax2.grid(True, linestyle='-')
        
        ax1.yaxis.label.set_color('b')
        ax1.yaxis.label.set_fontsize(16)
        ax2.yaxis.label.set_color('b')
        ax2.yaxis.label.set_fontsize(16)
        
        ax1.set_ylabel(DP11)
        ax2.set_ylabel(DP21)
        print ("get data done!")
        
    # If the first datapoint of the 2nd subplot is null then only create 1 subplot
    else:
        ax1 = plt.subplot2grid((1,1),(0,0), rowspan=1, colspan=1)
        if DP12 != 'Null':
            ax1v = ax1.twinx()
        
        ax1.set_title('RV Solar Data')

        # query the database and process 1 datapoint on the 1st and only subplot
        if DP12 == 'Null':
            DBcursor.execute("SELECT [Date Time], [%s] FROM [Raw Solar Data] WHERE [Date Time] >= ? AND [Date Time] <= ?" % (DP11), (SD,ED))
            for row in DBcursor.fetchall():
                x1.append(mdates.datestr2num(row[0]))
                y11.append(row[1])
            for label in ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(True)
                ax1.set_prop_cycle('color', ['red', 'blue'])
            plt.subplots_adjust(left=0.1, bottom=0.12, right=0.94, top=0.94, wspace=0.2, hspace=0.07)

        # query the database and process 2 datapoints on the 1st and only subplot
        if DP12 != 'Null':
            DBcursor.execute("SELECT [Date Time], [%s], [%s] FROM [Raw Solar Data] WHERE [Date Time] >= ? AND [Date Time] <= ?" % (DP11, DP12), (SD,ED))
            for row in DBcursor.fetchall():
                x1.append(mdates.datestr2num(row[0]))
                y11.append(row[1])
                y12.append(row[2])
            for label in ax1.xaxis.get_ticklabels():
                label.set_rotation(45)
                label.set_horizontalalignment('right')
                label.set_visible(True)
                ax1v.set_prop_cycle('color', ['blue', 'red'])
                ax1v.yaxis.label.set_color('b')
                ax1v.plot_date(x1,y12, '-', label=DP12)
                ax1v.set_ylabel(DP12)
                ax1v.minorticks_on()
            plt.subplots_adjust(left=0.1, bottom=0.12, right=0.9, top=0.94, wspace=0.2, hspace=0.07)

        xfmt = mdates.DateFormatter('%Y-%m-%d %H:%M')
        ax1.xaxis.set_major_formatter(xfmt)
        ax1.set_prop_cycle('color', ['red', 'blue'])
        ax1.plot_date(x1,y11, '-', label=DP11)
        ax1.grid(True, linestyle='-')
        ax1.yaxis.label.set_color('r')
        ax1.set_ylabel(DP11)
        ax1.minorticks_on()

# End Of Get and plot data function
#-----------------------------------------------

# Setup the data points you want to plot
DPoint_ax11 = 'Null'
DPoint_ax11 = 'Voltage'
#DPoint_ax11 = 'Filtered Voltage'
#DPoint_ax11 = 'Voltage B2'
#DPoint_ax11 = 'Amperage'
#DPoint_ax11 = 'Filtered Amperage'
#DPoint_ax11 = 'Amp Hours'
#DPoint_ax11 = 'Percentage'
#DPoint_ax11 = 'Watts'
#DPoint_ax11 = 'Days Since Charged'
#DPoint_ax11 = 'Days Since Equalized'

DPoint_ax12 = 'Null'
#DPoint_ax12 = 'Voltage'
#DPoint_ax12 = 'Filtered Voltage'
#DPoint_ax12 = 'Voltage B2'
DPoint_ax12 = 'Amperage'
#DPoint_ax12 = 'Filtered Amperage'
#DPoint_ax12 = 'Amp Hours'
#DPoint_ax12 = 'Percentage'
#DPoint_ax12 = 'Watts'
#DPoint_ax12 = 'Days Since Charged'
#DPoint_ax12 = 'Days Since Equalized'

DPoint_ax21 = 'Null'
#DPoint_ax21 = 'Voltage'
#DPoint_ax21 = 'Filtered Voltage'
#DPoint_ax21 = 'Voltage B2'
#DPoint_ax21 = 'Amperage'
#DPoint_ax21 = 'Filtered Amperage'
DPoint_ax21 = 'Amp Hours'
#DPoint_ax21 = 'Percentage'
#DPoint_ax21 = 'Watts'
#DPoint_ax21 = 'Days Since Charged'
#DPoint_ax21 = 'Days Since Equalized'

DPoint_ax22 = 'Null'
#DPoint_ax22 = 'Voltage'
#DPoint_ax22 = 'Filtered Voltage'
#DPoint_ax22 = 'Voltage B2'
#DPoint_ax22 = 'Amperage'
#DPoint_ax22 = 'Filtered Amperage'
#DPoint_ax22 = 'Amp Hours'
#DPoint_ax22 = 'Percentage'
DPoint_ax22 = 'Watts'
#DPoint_ax22 = 'Days Since Charged'
#DPoint_ax22 = 'Days Since Equalized'

#------------------------------------------------------------------
#NumberOfWeeks = 4
#DateTimeDelta = dt.timedelta(weeks = NumberOfWeeks)

#NumberOfDays = 1
#DateTimeDelta = dt.timedelta(days = NumberOfDays)

#NumberOfHours = 10
#DateTimeDelta = dt.timedelta(hours = NumberOfHours)

#NumberOfMin = 30
#DateTimeDelta = dt.timedelta(minutes = NumberOfMin)

#EndDateTime = dt.datetime.now()
#EndDate = str(dt.datetime.now()) [0:-7]
#StartDate = str(EndDateTime - DateTimeDelta) [0:-7]
#------------------------------------------------------------------

GetYearStart = 2018
GetYearEnd = 2018

GetMonthStart = 4
GetMonthEnd = 4

GetDayStart = 15
GetDayEnd = 15

GetHourStart = 8
GetHourEnd = 11

GetMinStart = 0
GetMinEnd = 59

StartDate = str(dt.datetime(GetYearStart, GetMonthStart, GetDayStart, GetHourStart, GetMinStart))
EndDate = str(dt.datetime(GetYearEnd, GetMonthEnd, GetDayEnd, GetHourEnd, GetMinEnd))

#----------------------------------------------------------------------

# Call the function with the arguments
print ("function called")
GetDataAndPlot(StartDate, EndDate, DPoint_ax11, DPoint_ax21, DPoint_ax12, DPoint_ax22)
plt.tight_layout()
plt.show()
