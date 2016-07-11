from __future__ import print_function
import httplib2
import os
import json

import sys
sys.path.insert(1, '/Library/Python/2.7/site-packages')

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

application_path = os.path.dirname(__file__)
dbFilePath = os.path.join(application_path, 'db.db')

# Used for retrieve_meetup_calendar function

import requests
import time

class Model(object):
    @classmethod
    def retrieve_meetup_calendar(cls, x):
        meetup_events = requests.get(x)
        meetup_events1 = meetup_events.json()
#        events_meetup = meetup_events1['results']
        events_meetup = meetup_events1.get('results', [])

        for event in events_meetup:
            time_since = (event['time'])
            time = datetime.datetime.fromtimestamp(time_since/1000).strftime('%Y-%m-%d %H:%M:%S')
            Start_Time = datetime.datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
            event.update(
                {'time':
                    {
                        'year': Start_Time.strftime("%Y"),
                        'month': Start_Time.strftime("%b"),
                        'day': Start_Time.strftime("%d"),
                        'hour': Start_Time.strftime("%H"),
                        'minute': Start_Time.strftime("%M"),
                        'second': Start_Time.strftime("%S")}})


        return(events_meetup)

    @classmethod
    def retrieve_calendar(cls):
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
            flow.user_agent = 'Google Calendar API Python Quickstart'
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:
                credentials = tools.run(flow, store)

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)

        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time (# Find time)
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        for event in events:

            Start_Date_Time_and_TimeZone = event['start'].get('dateTime', event['start'].get('date'))
            Start_Date_Time_and_TimeZone_List = Start_Date_Time_and_TimeZone.partition('+')
            if len(Start_Date_Time_and_TimeZone_List[0]) >= 11:
                Start_Date_and_Time = datetime.datetime.strptime(Start_Date_Time_and_TimeZone_List[0], '%Y-%m-%dT%H:%M:%S')
                event.update(
                    {'start':
                         {
                             'year': Start_Date_and_Time.strftime("%Y"),
                             'month': Start_Date_and_Time.strftime("%b"),
                             'day': Start_Date_and_Time.strftime("%d"),
                             'hour': Start_Date_and_Time.strftime("%H"),
                             'minute': Start_Date_and_Time.strftime("%M"),
                             'second': Start_Date_and_Time.strftime("%S")}})
            else:
                Start_Date = datetime.datetime.strptime(Start_Date_Time_and_TimeZone_List[0], '%Y-%m-%d')
                event.update(
                    {'start':
                        {
                            'year': Start_Date.strftime("%Y"),
                            'month': Start_Date.strftime("%b"),
                            'day': Start_Date.strftime("%d")}})


            End_Date_Time_and_TimeZone = event['end'].get('dateTime', event['end'].get('date'))
            End_Date_Time_and_TimeZone_List = End_Date_Time_and_TimeZone.partition('+')
            if len(End_Date_Time_and_TimeZone_List[0]) >= 11:
                End_Date_and_Time = datetime.datetime.strptime(End_Date_Time_and_TimeZone_List[0], '%Y-%m-%dT%H:%M:%S')
                event.update(
                    {'end':
                        {
                            'year': End_Date_and_Time.strftime("%Y"),
                            'month': End_Date_and_Time.strftime("%m"),
                            'day': End_Date_and_Time.strftime("%d"),
                            'hour': End_Date_and_Time.strftime("%H"),
                            'minute': End_Date_and_Time.strftime("%M"),
                            'second': End_Date_and_Time.strftime("%S")}})
            else:
                End_Date = datetime.datetime.strptime(End_Date_Time_and_TimeZone_List[0], '%Y-%m-%d')
                event.update(
                    {'end':
                        {
                            'year': End_Date.strftime("%Y"),
                            'month': End_Date.strftime("%m"),
                            'day': End_Date.strftime("%d")}})
        return events