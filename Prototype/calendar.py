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
SCOPES = 'https://www.googleapis.com/auth/calendar'

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
        
def freetimeevent():
    service = connection.googleCalendar(SCOPES)
    
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='t4p9h18kn9ka3nf8sf6teobfbfouoo6t@import.calendar.google.com',
                                        timeMin=now,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        
    end_time = datetime.datetime.now()
    for event in events:
        
        start_string = calhelp.time2str(end_time) #curr start time is the prev end time
        print(start_string)
        _,_, is_whole_day = calhelp.getEventStartEnd(event)
        print(is_whole_day)
        
        if is_whole_day:
            continue
        else:
            start_time,end_time,_ = calhelp.getEventStartEnd(event)
        end_string = calhelp.time2str(start_time) #the curr end time is the next start time
        
        print(start_string)
        print(end_string)
        new_event = {
                "start":{"dateTime":start_string},
                "end":{"dateTime":end_string},
                "summary":"Free Time",
                }
        
        service.events().insert(calendarId = "primary",body = new_event).execute()

def AllocateSleep():
    service = connection.googleCalendar(SCOPES)
    today = datetime.date.today()
    time_begin = datetime.time(23,30,0)
    duration = datetime.timedelta(hours = 8.0)
    datetime_begin = datetime.datetime.combine(today,time_begin)
    datetime_end = datetime_begin + duration
    for days in range(5):
        datetime_begin = datetime_begin + datetime.timedelta(days = 1)
        datetime_end = datetime_end + datetime.timedelta(days = 1)
        start_string = calhelp.time2str(datetime_begin)
        end_string = calhelp.time2str(datetime_end)
        
        print(start_string)
        sleep_event = calhelp.eventCreator(start_string,end_string,0,-1,"Health",5,5,"Sleep",-2)
        service.events().insert(calendarId = "primary",body = sleep_event).execute()
        
        print('Event Created')
        
def check_free_time():
    service = connection.googleCalendar(SCOPES)
    free_times = calhelp.freeTimeChecker(service)
    for free_time in free_times:
        start = free_time['start']['dateTime']
        duration = free_time['duration']
        print('Free time: ' + str(duration) + 'mins ' + str(start))
if __name__ == '__main__':
    #AllocateSleep()
    check_free_time()