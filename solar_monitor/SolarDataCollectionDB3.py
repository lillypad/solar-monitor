#!/usr/bin/env python
# Solar Data Collection.py
# Written by John Chalupowski
# Development enviroment  Idle (Python 3)

#Version 1.0 2017-07-01
#Version 1.1 2017-07-09
#Version 1.2 2017-07-17

# Import the necessary modules
import serial
import datetime
import time
import os
import re
import sys
import sqlite3

#sys.stdout = open('solar.log', 'a')

# setup serial port for reading
port = serial.Serial("/dev/ttyUSB0", baudrate=2400, timeout=3.0)
# read 50 bytes of data from serial port. this ensures we don't save any preamble
trash = port.read(50)

# initialize variables and 1st run assignments.
savepath = "/media/pi/SOLARUSB/SolarData/"
dbpath = "/media/pi/SOLARUSB/SolarMonitor/"
dbfile = "SolarDataCollection.db"
lastsaved = 60
saveinterval = 2 # Save every x minutes

# Create database file
DBconnect = sqlite3.connect(dbpath + dbfile)
DBcursor = DBconnect.cursor()
DBOpen = 1

### CreateTable Function Code
##def CreateTable():
##    DBcursor.execute('''CREATE TABLE IF NOT EXISTS Raw_Solar_Data (ID INTEGER PRIMARY KEY, Date_Time TEXT, Voltage_B1 REAL, Filtered_Voltage REAL, Voltage_B2 REAL, Amperage REAL, Filtered_Amperage REAL, Amp_Hours REAL, Percentage INTEGER, Watts REAL, DSC REAL, DSE REAL)''')
##
### AddData Function Code
##def AddData(Date_Time,Voltage_B1,Filtered_Voltage,Voltage_B2,Amperage,Filtered_Amperage,Amp_Hours,Percentage,Watts,DSC,DSE):
##    DBcursor.execute('''INSERT INTO Raw_Solar_Data (Date_Time,Voltage_B1,Filtered_Voltage,Voltage_B2,Amperage,Filtered_Amperage,Amp_Hours,Percentage,Watts,DSC,DSE)
##    VALUES (?,?,?,?,?,?,?,?,?,?,?)''',(Date_Time,Voltage_B1,Filtered_Voltage,Voltage_B2,Amperage,Filtered_Amperage,Amp_Hours,Percentage,Watts,DSC,DSE))

# CreateTable Function Code
def CreateTable():
    DBcursor.execute("CREATE TABLE IF NOT EXISTS 'Raw Solar Data' (ID INTEGER PRIMARY KEY, 'Date Time' TEXT, 'Voltage' REAL, 'Filtered Voltage' REAL, 'Voltage B2' REAL, 'Amperage' REAL, 'Filtered Amperage' REAL, 'Amp Hours' REAL, 'Percentage' INTEGER, 'Watts' REAL, 'Days Since Charged' REAL, 'Days Since Equalized' REAL)")
    
# AddData Function Code
def AddData(Date_Time,Voltage_B1,Filtered_Voltage,Voltage_B2,Amperage,Filtered_Amperage,Amp_Hours,Percentage,Watts,DSC,DSE):
    DBcursor.execute('''INSERT INTO 'Raw Solar Data' ('Date Time','Voltage','Filtered Voltage','Voltage B2','Amperage','Filtered Amperage','Amp Hours','Percentage','Watts','Days Since Charged','Days Since Equalized')
    VALUES (?,?,?,?,?,?,?,?,?,?,?)''',(Date_Time,Voltage_B1,Filtered_Voltage,Voltage_B2,Amperage,Filtered_Amperage,Amp_Hours,Percentage,Watts,DSC,DSE))

# Create The Database Table
CreateTable()


# main program loop
while True:
    rcv = port.read(100) # read 100 bytes of data from serial port. this ensures we have a complete set of data
    minute = int(datetime.datetime.now().strftime("%M"))

    if minute % saveinterval == 0  and lastsaved  != minute:
        UnixTimeData = time.time()
        DateTimeData = str(datetime.datetime.fromtimestamp(UnixTimeData).strftime('%Y-%m-%d %H:%M:%S'))
        #RawData = str (rcv) # convert the recieved data to a string called RawData
        
        # Create / Open database file
        if DBOpen == 0:
            DBconnect = sqlite3.connect(dbpath + dbfile)
            DBcursor = DBconnect.cursor()
        
        data = rcv.decode('utf-8') # convert the recieved data to a string called RawData
	#data = "FV=13.1,V2=00.0,A=10.6,FA=08.7,AH=-100.0,%=071,W=140,DSC=3.96,DSE=32.0,V=13.1,FV=13.1,V2=00.0,A=09.2,"
        #print(datetime.datetime.now().isoformat() + " - " + str(data))
        regV  = re.compile(r'(?<=\,V\=)\-?\d{1,}\.\d{1,}(?=\,)')
        regFV = re.compile(r'(?<=\,FV\=)\-?\d{1,}\.\d{1,}(?=\,)')
        regV2 = re.compile(r'(?<=\,V2\=)\-?\d{1,}\.\d{1,}(?=\,)')
        regA  = re.compile(r'(?<=\,A\=)\-?\d{1,}\.?\d{1,}(?=\,)')
        regFA = re.compile(r'(?<=\,FA\=)\-?\d{1,}\.?\d{1,}(?=\,)')
        regAH = re.compile(r'(?<=\,AH\=)\-?\d{1,}\.?\d{1,}?(?=\,)')
        regP  = re.compile(r'(?<=\,\%\=)\-?\d{1,}(?=\,)')
        regW  = re.compile(r'(?<=\,W\=)\-?\d{1,}\.?\d{1,}?(?=\,)')
        regDSC = re.compile(r'(?<=\,DSC\=)\-?\d{1,}\.?\d{1,}(?=\,)')
        regDSE = re.compile(r'(?<=\,DSE\=)\-?\d{1,}\.?\d{1,}?(?=\,)')
        Volts = FilteredVolts = Volts2 = Amps = FilteredAmps = AmpHours = BatteryPercentage = Watts = DSC = DSE = 0
        if bool(re.search(regV, data)):
                Volts = float(re.search(regV, data).group(0))
        if bool(re.search(regFV, data)):
                FilteredVolts = float(re.search(regFV, data).group(0))
        if bool(re.search(regV2, data)):
                Volts2 = float(re.search(regV2, data).group(0))
        if bool(re.search(regA, data)):
                Amps = float(re.search(regA, data).group(0))
        if bool(re.search(regFA, data)):
                FilteredAmps = float(re.search(regFA, data).group(0))
        if bool(re.search(regAH, data)):
                AmpHours = float(re.search(regAH, data).group(0))
        if bool(re.search(regP, data)):
                BatteryPercentage = int(re.search(regP, data).group(0))
        if bool(re.search(regW, data)):
                Watts = float(re.search(regW, data).group(0))
        if bool(re.search(regDSC, data)):
                DSC = float(re.search(regDSC, data).group(0))
        if bool(re.search(regDSE, data)):
                DSE = float(re.search(regDSE, data).group(0))
        
        AddData(DateTimeData,Volts,FilteredVolts,Volts2,Amps,FilteredAmps,AmpHours,BatteryPercentage,Watts,DSC,DSE)
        DBconnect.commit()
        DBcursor.close() #Close the database cursor
        DBconnect.close() # Close the database file
        DBOpen = 0
        lastsaved = minute
