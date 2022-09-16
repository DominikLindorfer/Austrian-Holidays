#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Time    :   2022/09/16 08:28:10
@Author  :   Dominik Lindorfer 
@Contact :   d.lindorfer@3bg.at
@License :   (C)Copyright
@Version :   0.1
@Descr   :   Calculate which Austrian Holidays take place on Weekdays or Weekends
'''
from calendar import weekday
import pandas as pd
from datetime import date
import holidays
import icalendar
import pytz
# from workalendar.europe import Austria

years = [2022 + i for i in range(19)] 

for year in years: 

    # if year != 2022:
    #     continue

    all_holidays = list(holidays.Austria(years=[year]).items())
    all_holidays.append((date(year, 12, 24), "Weihnachten"))
    # print(all_holidays)
    weekdays = 0
    weekends = 0
    zwickeltage = 0
    bridgedays = []

    for holiday in all_holidays:

        if holiday[0].weekday() > 4:
            weekends += 1
            # print("Weekends: ", holiday)
        else:
            weekdays += 1
            # print("Weekday: ", holiday)

        if holiday[0].weekday() == 3:
            # print("Bridgeday: ", holiday)
            zwickeltage += 1
            bridgedays.append(holiday)

    print("============")
    print("Year: ", year)
    print("============")
    print("Holidays on Weekdays: ", weekdays)
    print("Holidays on Weekends: ", weekends)
    print("Bridgedays: ", zwickeltage)
    print("===============")
    for bridgeday in bridgedays:
        print(bridgeday[1], "on " + str(bridgeday[0].month) + "." + str(bridgeday[0].day))

    print("\n")



