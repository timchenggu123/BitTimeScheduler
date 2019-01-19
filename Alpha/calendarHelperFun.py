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
                 importance, custom_name = -1, extensibility = 0, days_till_expire = 0,
                 time_zone = 'America/Toronto',cal_id = 'primary'):

    if custom_name == -1:
        custom_name = event_type
    
    if not type(start) is str:
        start = time2str(start)
    
    if not type(end) is str:
        end = time2str(end)
        
    event = {
            "start":{"dateTime":start,
                     "timeZone":time_zone},
            "end":{"dateTime":end,
                   "timeZone":time_zone},
            "summary": custom_name,
            }
    
    if type(expirary_date) is datetime.datetime :
        days_till_expire = expirary_date - str2time(start)
        days_till_expire = divmod(days_till_expire.total_seconds(),86400)[0]
        expirary_date = expirary_date.date()
        
    elif type(expirary_date) is datetime.date:
        days_till_expire = expirary_date - str2time(start).date()
        days_till_expire = days_till_expire.days
        
    elif expirary_date == str(-999):
        expirary_date = str2time(start).date()
        
    description_info = ("&reschedulability:" + str(reschedulability) +
                       "&expirary_date:" + str(expirary_date) +
                       "&days_till_expire:" + str(days_till_expire) +
                       "&event_type:" + str(event_type) +
                       "&urgency:" + str(urgency) +
                       "&importance:" + str(importance) +
                       "&extensibility:" + str(extensibility))
                        
    event['description'] = description_info
    event_duration_timedelta = str2time(end) - str2time(start)
    event_duration = divmod(event_duration_timedelta.total_seconds(),60)
    event_duration = event_duration[0]
    event['duration'] = event_duration
    event['cal_id'] = cal_id
    
    return event

def addCustomTags(event, description = '', custom_tags = {}):
    
    if description and not custom_tags:
        custom_tags = getCustomTags(description = description)
    elif description and custom_tags:
        raise ValueError('Too many arguments. Please only provid one')
        
    expirary_date = custom_tags['expirary_date']
    days_till_expire = custom_tags['days_till_expire']
    start = event['start']['dateTime']
    
    if type(expirary_date) is datetime.datetime :
        days_till_expire = expirary_date - str2time(start)
        days_till_expire = divmod(days_till_expire.total_seconds(),86400)[0]
        expirary_date = expirary_date.date()
        
    elif type(expirary_date) is datetime.date:
        days_till_expire = expirary_date - str2time(start).date()
        days_till_expire = days_till_expire.days
        
    elif expirary_date == str(-999):
        expirary_date = str2time(start).date()
    
    custom_tags['expirary_date'] = expirary_date
    custom_tags['days_till_expire'] = days_till_expire
    
    description_info = ''
    for custom_tag in custom_tags:
        custom_string = '&' + custom_tag +':'+str(custom_tags[custom_tag])
        description_info += custom_string
    
    event['description'] = description_info
    return event
    
def changeCustomTags(event,custom_tags):
    event_custom_tags = getCustomTags(event)
    
    for custom_tag in custom_tags:
        event_custom_tags[custom_tag] = custom_tags[custom_tag]
        
    description_info = ''
    for custom_tag in event_custom_tags:
        custom_string = '&' + custom_tag +':'+str(event_custom_tags[custom_tag])
        description_info += custom_string

    event['description'] = description_info
    
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
        
def getFreeTime(service,start_datetime = datetime.datetime.now(),check_ndays = 14,min_free_len_mins = 10):
    """returns a list of free time psuedo-events starting from start_date for 
    n effective_days
    
    service: googleCalendar API connection. See connection.py
    start_date: datetime.datetime obj
    effective_days: datetime.timedelta obj
    check_ndays: how many  days from the start date to check for
    min_free_len_mins: minumn lenth of free time. Any free time shorter will be ignored
    """
    calendar_result = service.calendarList().list().execute()
    calendars = calendar_result.get('items',[])
    all_events = []
    for calendar in calendars:
        cal_id = calendar['id']
        events = getEvents(service,cal_id,start_datetime,check_ndays)
        all_events = all_events + events
    
    #now we remove all day events
    remove_list = list()
    for event in all_events:
        if not event['start'].get('dateTime',0):
            remove_list.append(event)
            
    for event in remove_list:
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
           
           free_time = eventCreator(end_datetime,start_datetime,-2,0,'free event',0,0,'Free Time',0) #not the start_datetime field is actually filled by the end_datetime vairable, and vice versa
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
    end_datetime = start_datetime + datetime.timedelta(days = int(search_for_ndays) + 1) #+1 here because timeMax is exclusive
    
    start_datetime = utcFormat(start_datetime)
    end_datetime = utcFormat(end_datetime)
    events_result = service.events().list(calendarId= calId,
                                        timeMin=start_datetime,
                                        maxResults= 1000, singleEvents=True,
                                        timeMax= end_datetime,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    return events

def getEventDuration(event):
    start = event['start'].get('dateTime')
    end = event['end'].get('dateTime')
    event_duration_timedelta = str2time(end) - str2time(start)
    event_duration = divmod(event_duration_timedelta.total_seconds(),60)
    event_duration = round(event_duration[0])
    
    return event_duration
    
    
def getAllEvents(service,start_datetime,search_for_ndays,cal_presets = {}):
    calendar_result = service.calendarList().list().execute()
    calendars = calendar_result.get('items',[])
    all_events = []
    for calendar in calendars:
        cal_id = calendar['id']
        events = getEvents(service,cal_id,start_datetime,search_for_ndays)
        
        for event in events:
            event['cal_id'] = cal_id
            if 'description' in event:
                if not hasCustomTags(event) and cal_presets:
                    for cal_preset in cal_presets:
                        if cal_preset['cal_id'] == cal_id:
                            event['description'] = cal_preset['description']
                            
                    if not event['description']:
                        raise ValueError('Calendar preset description info missing for ' + cal_id)
                        
                elif not event['description']: #in the case when there no description and cal_preset is empty...
                    raise ValueError('Calendar preset description info missing for ' + cal_id)
            elif len(cal_presets) > 0:
                for cal_preset in cal_presets:
                    if cal_preset['cal_id'] == cal_id:
                        addCustomTags(event,cal_preset['description'])                    
            else:
                raise ValueError('Calendar preset description info missing for ' + cal_id)
                    
        all_events = all_events + events
        #now we remove all day events
    remove_list = list()
    for event in all_events:
        if not event['start'].get('dateTime',0):
            remove_list.append(event)
    for event in remove_list:
        all_events.remove(event)
     
    for event in all_events:
        if not event['start'].get('dateTime',0):
            stop = 1
    #now we sort all events by their start time
    all_events = sorted(all_events, key = lambda t: t['start'].get('dateTime'))
    
    return all_events
def hasCustomTags(event):
    if 'description' in event:
        custom_tags = getCustomTags(event)
        if 'days_till_expire' in custom_tags:
            return True
    return False

def utcFormat(DST_datetime):
    local = pytz.timezone ("America/Toronto")
    local_dt = local.localize(DST_datetime, is_dst=True)
    utc_dt = local_dt.astimezone(pytz.utc)
    utc_dt = utc_dt.isoformat()
    utc_dt = utc_dt[0:len(utc_dt)-6] + 'Z'
    return utc_dt

def getCustomTags(event = {},description = ''):
    if event:
        string = event['description']
    elif description:
        string = description
    else:
        raise ValueError('not enough arguments')
    
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
        try:
            custom_value = string[(key1+1):keys[i+1]]
        except:
            custom_value = string[(key1+1):len(string)]
        
        custom_tags[custom_field] = custom_value
        
    return custom_tags

def calcEventExpireDays(event):
    custom_tags = getCustomTags(event)
    expirary_date = custom_tags['expirary_date']
    start = event['start']['dateTime']
    days_till_expire = int(custom_tags['days_till_expire'])
    
    if expirary_date == str(0):
        expirary_date = str2time(start).date() + datetime.timedelta(days = days_till_expire)
    
    elif expirary_date == str(-999):
        expirary_date = str2time(start).date()
        
    else:
        try:
            expirary_date = str2time(expirary_date).date()
        except:
            raise ValueError('expirary date format invalid')

    today = datetime.date.today()
    expire_days = expirary_date - today
    expire_days = expire_days.days
    
    return expire_days
    
    
def updateEvent(service,event):
    if 'id' in event:
        updated_event = service.events().update(calendarId=event['cal_id'], eventId=event['id'], body=event).execute()
        print (updated_event['updated'])
    else:
        insertEvent(service,event)
        
def dropEvent(service,event):
    confirm = input('Event drop proposed. Do you want to drop event ' + event['summary'] + ' on ' + event['start']['dateTime'] + '?')
    if not confirm:
        return False
    to_be_dropped = service.events().delete(calendarId = event['cal_id'],eventId = event['id']).execute()
    print('Event ' + to_be_dropped['summary'] + 'is dropped')
    
    return True

def insertEvent(service,event):
    to_be_inserted = service.events().insert(calendarId = event['cal_id'],body = event).execute()
    print()
    print('Event ' + to_be_inserted['summary'] + ' has been created. link: %s' % (to_be_inserted.get('htmlLink')))
    print()
    
def createRecurringEvent(event,by_day ='MO,TU,WE,TH,FR,SA,SU',until = 0):
    '''until needs to be a string in the formta "YYYYMMDD" '''
    '''needs more work'''
    event['recurrence'] = list()
    
    if until:
        until_statement = 'UNTIL=' + until + ';'
    else:
        until_statement = ''
        
    event['recurrence'].append( 'RRULE:FREQ=WEEKLY;'+ until_statement+'BYDAY=' + by_day)
    return event


    


    

    



