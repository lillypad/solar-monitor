#!/usr/bin/env python
# Solar Data Collection.py
# Written by John Chalupowski
# Development enviroment  Idle (Python 3)

# Version 1.0 2017-07-01
# Version 1.1 2017-07-09
# Version 1.2 2017-07-17

# Import the necessary modules
import serial
import datetime
import re
import sqlite3

BUFFER_SIZE = 100
BUFFER_TRASH_SIZE = 50

regV = re.compile(r'(?<=\,V\=)\-?\d{1,}\.\d{1,}(?=\,)')
regFV = re.compile(r'(?<=\,FV\=)\-?\d{1,}\.\d{1,}(?=\,)')
regV2 = re.compile(r'(?<=\,V2\=)\-?\d{1,}\.\d{1,}(?=\,)')
regA = re.compile(r'(?<=\,A\=)\-?\d{1,}\.?\d{1,}(?=\,)')
regFA = re.compile(r'(?<=\,FA\=)\-?\d{1,}\.?\d{1,}(?=\,)')
regAH = re.compile(r'(?<=\,AH\=)\-?\d{1,}\.?\d{1,}?(?=\,)')
regP = re.compile(r'(?<=\,\%\=)\-?\d{1,}(?=\,)')
regW = re.compile(r'(?<=\,W\=)\-?\d{1,}\.?\d{1,}?(?=\,)')
regDSC = re.compile(r'(?<=\,DSC\=)\-?\d{1,}\.?\d{1,}(?=\,)')
regDSE = re.compile(r'(?<=\,DSE\=)\-?\d{1,}\.?\d{1,}?(?=\,)')

# sys.stdout = open('solar.log', 'a')

# setup serial port for reading
port = serial.Serial("/dev/ttyUSB0", baudrate=2400, timeout=3.0)
# read 50 bytes of data from serial port.
# This ensures we don't save any preamble
trash = port.read(BUFFER_TRASH_SIZE)

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


def CreateTable():
    """
    :TODO: Initalize Tables
    :returns: True
    """
    try:
        query = (
            "CREATE TABLE IF NOT EXISTS 'Raw Solar Data' (ID INTEGER PRIMARY "
            "KEY, 'Date Time' TEXT, 'Voltage' REAL, 'Filtered Voltage' REAL, "
            "'Voltage B2' REAL, 'Amperage' REAL, 'Filtered Amperage' REAL, "
            "'Amp Hours' REAL, 'Percentage' INTEGER, 'Watts' REAL, 'Days Since"
            " Charged' REAL, 'Days Since Equalized' REAL)"
        )
        DBcursor.execute(query)
        return True
    except Exception as e:
        raise e


def AddData(data_frame):
    """
    :TODO: Insert Data Frame into DB
    :returns: True
    """
    try:
        insert = (
            "INSERT INTO 'Raw Solar Data' ('Date Time','Voltage',"
            "'Filtered Voltage','Voltage B2','Amperage','Filtered Amperage',"
            "'Amp Hours','Percentage','Watts','Days Since Charged',"
            "'Days Since Equalized') VALUES (?,?,?,?,?,?,?,?,?,?,?)"
        )
        DBcursor.execute(
            insert,
            (
                data_frame['date_time'],
                data_frame['voltage_b1'],
                data_frame['filtered_voltage'],
                data_frame['voltage_b2'],
                data_frame['amperage'],
                data_frame['filtered_amperage'],
                data_frame['amp_hours'],
                data_frame['percentage'],
                data_frame['watts'],
                data_frame['dsc'],
                data_frame['dse']
            )
        )
        return True
    except Exception as e:
        raise e


def ParseRawData():
    """
    :TODO: Parse Raw Data to Data Frame
    :returns: JSON data_frame
    """
    try:
        if bool(re.search(regV, data)):
                volts = float(re.search(regV, data).group(0))
        else:
            volts = 0
        if bool(re.search(regFV, data)):
                filtered_volts = float(re.search(regFV, data).group(0))
        else:
            filtered_volts = 0
        if bool(re.search(regV2, data)):
                volts_2 = float(re.search(regV2, data).group(0))
        else:
            volts_2 = 0
        if bool(re.search(regA, data)):
                amps = float(re.search(regA, data).group(0))
        else:
            amps = 0
        if bool(re.search(regFA, data)):
                filtered_amps = float(re.search(regFA, data).group(0))
        else:
            filtered_amps = 0
        if bool(re.search(regAH, data)):
                amp_hours = float(re.search(regAH, data).group(0))
        else:
            amp_hours = 0
        if bool(re.search(regP, data)):
                battery_percentage = int(re.search(regP, data).group(0))
        else:
            battery_percentage = 0
        if bool(re.search(regW, data)):
                watts = float(re.search(regW, data).group(0))
        else:
            watts = 0
        if bool(re.search(regDSC, data)):
                dsc = float(re.search(regDSC, data).group(0))
        else:
            dsc = 0
        if bool(re.search(regDSE, data)):
                dse = float(re.search(regDSE, data).group(0))
        else:
            dse = 0
        data_frame = {
            'date_time': datetime.datetime.now().isoformat(),
            'volts': volts,
            'filtered_volts': filtered_volts,
            'volts_2': volts_2,
            'amps': amps,
            'filtered_amps': filtered_amps,
            'amp_hours': amp_hours,
            'battery_precentage': battery_percentage,
            'watts': watts,
            'dsc': dsc,
            'dse': dse
        }
        return data_frame
    except Exception as e:
        raise e


def main():
    try:
        CreateTable()
        while True:
            rcv = port.read(BUFFER_SIZE)
            minute = int(datetime.datetime.now().strftime("%M"))
            if minute % saveinterval == 0  and lastsaved  != minute:
                if DBOpen == 0:
                    DBconnect = sqlite3.connect(dbpath + dbfile)
                    DBcursor = DBconnect.cursor()
                data = rcv.decode('utf-8')
                data_frame = ParseRawData(data)
                AddData(data_frame)
                DBconnect.commit()
                DBcursor.close()
                DBconnect.close()
                DBOpen = 0
                lastsaved = minute
    except Exception as e:
        raise e


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        raise e
