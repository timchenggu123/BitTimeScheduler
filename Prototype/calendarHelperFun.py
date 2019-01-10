import datetime, pytz

def str2time(string):

    
    if len(string) > 10:
        nchar = len(string)
        string = string[0:nchar -6] # -6 to get ride of the -05:00 trailler
        timeformat = ('%Y-%m-%dT%H:%M:%S')
        
        dt = datetime.datetime.strptime(string, timeformat)
    else:
        timeformat = ('%Y-%m-%d')
        
        dt = datetime.datetime.strptime(string,timeformat)
    
    return dt

def time2str(datetime):
    timeformat = ('%Y-%m-%dT%H:%M:%S-05:00')
    
    return(datetime.strftime(timeformat))
    
def minsLeftinWeek():
    now = datetime.datetime.now()
    day = now.weekday()
    week_remain_days = 6 - day
    
    day_remain_mins = datetime.datetime.fromordinal(
                        datetime.date.today().toordinal())
    day_remain_mins = now - day_remain_mins
    day_remain_mins = divmod(day_remain_mins.total_seconds(),60)
    day_remain_mins = 24*60 - (day_remain_mins[0] + day_remain_mins[1])
    
    total_remain_mins = week_remain_days * 24 * 60 + day_remain_mins

    print('You have ' + str(total_remain_mins) + ' minutes left this week!')
    

def getEventStartEnd(event):
    '''returns start time & end time as datetime objects from an event struct'''
    
    start_string = event['start'].get('dateTime',event['start'].get('date'))
    start_time = str2time(start_string)
    
    end_string = event['end'].get('dateTime',0)
    
    whole_day_event = 0
    if not end_string:
        end_time = start_time + datetime.timedelta(days = 1)
        whole_day_event = 1
    else:
        end_time = str2time(end_string)
        
    return start_time,end_time,whole_day_event

def eventCreator(start, end, reschedulability, 
                 expirary_date, event_type, urgency,
                 importance, custom_name = -1, extensibility = 0):

    if custom_name == -1:
        custom_name = event_type
    
    if not type(start) is str:
        start = time2str(start)
    
    if not type(end) is str:
        end = time2str(end)
        
    event = {
            "start":{"dateTime":start},
            "end":{"dateTime":end},
            "summary": custom_name,
            }
    
    description_info = ("&reschedulability:" + str(reschedulability) +
                       "&expirary_date:" + str(expirary_date) +
                       "&event_type:" + str(event_type) +
                       "&urgency:" + str(urgency) +
                       "&importance:" + str(importance) )
    
    event['description'] = description_info
    event_duration_timedelta = str2time(end) - str2time(start)
    event_duration = divmod(event_duration_timedelta.total_seconds(),60)
    event_duration = event_duration[0]
    event['duration'] = event_duration
    
    return event

def daily_insert(service,event,time_begin,duration,
                 effective_days,date_start = datetime.datetime.today(),
                 repeat_on_day_of_week = {0,1,2,3,4,5,6}):
    """
    
        service: googleCalendar API connection. See connection.py
        event: event struct. Can be created from eventCreator()
        ***Note that event does not need to contain start and end dates. If it
        does, then it is going to overwritten***
        
        repeat_on_day_of_week: an integer list with len 1~7 and values 0-6 each integer
            value represent a day of week. e.g. 0 is Monday, 2 is Wednesday, etc. This determines
            on what day of the week the event shall repeat
        time_start: datetime.time() object. When the event take place on each day
        even_duartion: datetime.timedelta() object. Duration of the event
        effective_days: over how many days do you want the event repeated? e.g. 365 days (1 year)
        date_start (optional) : when do you want the event to start repeating? By default it is
            going to be the date when this function is executed. Note that if the day is not 
            one of the day specified in repeat_day_of_week, the next closest date meeting the 
            criterial is when the event going to start. 
        """

    datetime_begin = datetime.datetime.combine(date_start,time_begin)
    datetime_end = datetime_begin + duration
    
    for days in range(effective_days):
        datetime_begin = datetime_begin + datetime.timedelta(days = 1)
        datetime_end = datetime_end + datetime.timedelta(days = 1)
        
        #check if right weekday
        if not datetime_begin.weekday() in repeat_on_day_of_week:
            continue
        
        start_string = time2str(datetime_begin)
        end_string = time2str(datetime_end)
        
        event['start']['dateTime'] = start_string
        event['end']['dateTime'] = end_string
        service.events().insert(calendarId = "primary",body = event).execute()
        
def freeTimeChecker(service,check_ndays = 14,start_datetime = datetime.datetime.now() ,min_free_len_mins = 10):
    """returns a list of free time psuedo-events starting from start_date for 
    n effective_days
    
    service: googleCalendar API connection. See connection.py
    start_date: datetime.datetime obj
    effective_days: datetime.timedelta obj
    check_ndays: how many  days from the start date to check for
    min_free_len_mins: minumn lenth of free time
    """
    calendar_result = service.calendarList().list().execute()
    calendars = calendar_result.get('items',[])
    all_events = []
    for calendar in calendars:
        cal_id = calendar['id']
        events = getEvents(service,cal_id,start_datetime,check_ndays)
        all_events = all_events + events
    
    #now we remove all day events
    for event in all_events:
        if not event['start'].get('dateTime',0):
            all_events.remove(event)
    #now we sort all events by their start time
    all_events = sorted(all_events, key = lambda t: t['start'].get('dateTime'))
    
    #we set the first end time to be start_time
    end_datetime = start_datetime
    #create a list holder of free_time events
    free_times = []
    for event in all_events:
        start_string = event['start']['dateTime']
        start_datetime = str2time(start_string)
        
        duration_timedelta = start_datetime - end_datetime #we calculate duration by using the start time of the second event minus the end time of the first event
        duration = divmod(duration_timedelta.total_seconds(),60)
        duration = duration[0]
        
        if duration < min_free_len_mins:
            # if duration is too short skip
            end_datetime = str2time(event['end']['dateTime'])
            continue
        else:
            #if duration is good, create free time event
           
           free_time = eventCreator(end_datetime,start_datetime,5,0,'free event',0,0,0,0) #not the start_datetime field is actually filled by the end_datetime vairable, and vice versa
           free_times.append(free_time)
        #update end_datetime for next loop
        end_datetime = str2time(event['end']['dateTime'])
        
        
    return free_times

def getCalendarId(service,calendar_summary):
    '''returns a calendar_Id from a calendar_summary. Always returns the 
    first one found. If none found, return -1'''
    
    calendar_result = service.calendarList().list().execute()
    calendars = calendar_result.get('items',[])
    for calendar in calendars:
        if calendar['summary'] == calendar_summary:
            return calendar['id']
        
    return -1
        
def getEvents(service,calId,start_datetime,search_for_ndays):
    end_datetime = start_datetime + datetime.timedelta(days = search_for_ndays)
    
    start_datetime = utcFormat(start_datetime)
    end_datetime = utcFormat(end_datetime)
    events_result = service.events().list(calendarId= calId,
                                        timeMin=start_datetime,
                                        maxResults= 1000, singleEvents=True,
                                        timeMax= end_datetime,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def utcFormat(DST_datetime):
    local = pytz.timezone ("America/Toronto")
    local_dt = local.localize(DST_datetime, is_dst=True)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt = utc_dt.isoformat()
    utc_dt = utc_dt[0:len(utc_dt)-6] + 'Z'
    return utc_dt

def getCustomTags(event):
    string = event['description']
    
    keys = []
    keys1 = []
    key = -1
    key1 = -1
    while  True:
        key = string.find('&',key+1)
        if key == -1:
            break
        keys.append(key)
        key1 = string.find(':',key1+1)
        keys1.append(key1)

    custom_tags = {}
    for i in range(len(keys)):

        key = keys[i]
        key1 = keys1[i]
        custom_field = string[(key+1):key1]
        print(key)
        print(key1)
        print(custom_field)
        try:
            custom_value = string[(key1+1):keys[i+1]]
        except:
            custom_value = string[(key1+1):len(string)]
        
        custom_tags[custom_field] = custom_value
        
    return custom_tags
    
    

                       



