#house keeping modeules for google calendar API carried over from quickstart.py
from __future__ import print_function
import datetime 
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

#additional modules
import calendarHelperFun as calhelp
import connection 

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'

def main():
    service = connection.googleCalendar(SCOPES)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='t4p9h18kn9ka3nf8sf6teobfbfouoo6t@import.calendar.google.com',
                                        timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start_string = event['start'].get('dateTime',event['start'].get('date'))
        end_string = event['end'].get('dateTime',0)
        
        start_time = calhelp.str2time(start_string)
        
        if not end_string:
            end_time = start_time + datetime.timedelta(days = 1)
        else:
            end_time = calhelp.str2time(end_string)
        
        duration = end_time - start_time
        duration_mins = divmod(duration.total_seconds(),60)
        duration_mins = duration_mins[0] + duration_mins[1]
        print(duration_mins, event['summary'])
        
def freetimecheck():
    service = connection.googleCalendar(SCOPES)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='t4p9h18kn9ka3nf8sf6teobfbfouoo6t@import.calendar.google.com',
                                        timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start_time, end_time = calhelp.getEventStartEnd(event)
        duration = end_time - start_time
        duration_mins = divmod(duration.total_seconds(),60)
        duration_mins = duration_mins[0] + duration_mins[1]
        print(duration_mins, event['summary'])
        
        
if __name__ == '__main__':
    freetimecheck()