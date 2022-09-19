#!/usr/bin/env python
# -*-coding:utf-8 -*-
'''
@File    :   main.py
@Time    :   2022/09/16 08:28:10
@Author  :   Dominik Lindorfer 
@Contact :   dominik.lindorfer@posteo.at
@License :   (C)Copyright
@Version :   0.1
@Descr   :   Calculate which Austrian Holidays take place on Weekdays or Weekends
'''
from calendar import weekday
import pandas as pd
from datetime import date, timedelta
import holidays
import email as email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
import email.encoders
import smtplib
from email.utils import formatdate
import os, sys
import datetime
# from workalendar.europe import Austria

def send_invite(from_address, to_address, bridge_date, description = "", subject = "", smpt = None):
    
    msg = MIMEMultipart('mixed')
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "Termin Reminder: Zwickeltag am " + str(bridge_date)
    # msg['Subject'] = "Termin Reminder: " + str(bridge_date )
    msg['From'] = from_address
    msg['To'] = to_address

    __location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))
    f= os.path.join(__location__, 'invite.ics')   
    ics_content = open(f).read()

    bridge_datetime = datetime.datetime(bridge_date.year, bridge_date.month, bridge_date.day, 9, 0, 0)

    replaced_contents = ics_content.replace('startDate', (bridge_datetime - timedelta(weeks=3, minutes=5)).strftime("%Y%m%dT%H%M%SZ"))
    replaced_contents = replaced_contents.replace('endDate', (bridge_datetime - timedelta(weeks=3, minutes=0)).strftime("%Y%m%dT%H%M%SZ"))
    # replaced_contents = replaced_contents.replace('endDate', datetime.datetime(2022,9,20, 12, 35, 0).strftime("%Y%m%dT%H%M%SZ"))

    replaced_contents = replaced_contents.replace('telephonic', "")
    replaced_contents = replaced_contents.replace('now', datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ"))
    
    replaced_contents = replaced_contents.replace('describe', description)

    replaced_contents = replaced_contents.replace('attend',  msg['To'])
    replaced_contents = replaced_contents.replace('subject',  subject)
    
    # replaced_contents = replaced_contents.replace('startTrigger', "-PT{0}H".format(1))

    part_email = MIMEText(description,'calendar;method=REQUEST')
    
    msgAlternative = MIMEMultipart('alternative')
    
    ical_atch = MIMEBase('text/calendar',' ;name="%s"'%"invitation.ics")
    ical_atch.set_payload(replaced_contents)
    email.encoders.encode_base64(ical_atch)
    ical_atch.add_header('Content-Disposition', 'attachment; filename="Reminder.ics"')
    
    msgAlternative.attach(part_email)
    msgAlternative.attach(ical_atch)
    msg.attach(msgAlternative)
    
    # Send the email out
    smpt.sendmail(msg["From"], [msg["To"]], msg.as_string())

def get_holidays(year_range = 19, print_holidays = True):
    years = [2022 + i for i in range(year_range)] 
    all_bridgedays = {}

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

        all_bridgedays[str(year)] = bridgedays

        if print_holidays == True:
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

    return all_bridgedays

def send_email_reminders(all_bridgedays, config):

    smpt = config["smpt"]

    for item in all_bridgedays[str(config["year"])]:
        
        bridge_date = item[0]
        holiday_name = item[1]

        subject = "Bitte freinehmen fuer: " + str(bridge_date) + "!"
        description = "Am " + str(bridge_date) + " ist ein Zwickeltag (" + holiday_name + ")! Bitte freinehmen!"
        send_invite(to_address=config["to_address"], from_address=config["from_address"], bridge_date=bridge_date, description=description, subject=subject, smpt=smpt)

    smpt.quit()

if __name__ == "__main__":

    bridge_days = get_holidays(print_holidays=False)

    config = {
                "to_address" : "dominik.lindorfer@posteo.at",
                "from_address" : "Zwickeltag Reminder <dominik.lindorfer@posteo.at>",
                "smpt" : None,
                "year" : 2023
    }

    send_email_reminders(bridge_days, config)
