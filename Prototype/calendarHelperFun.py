import datetime 

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

def eventCreator(start_string, end_string, reschedulability, 
                 expirary_date, event_type, urgency,
                 importance, custom_name = -1)
    if custom_name == -1:
        custom_name = event_type
    event = {
            "start":{"dateTime":start_string},
            "end":{"dateTime":end_string},
            "summary": event_type,
            }
    
    description_info = ("&reschedulability:" + str(reschedulability) +
                       "&expirary_date:" + str(expirary_date) +
                       "&event_type:" + str(event_type) +
                       "&urgency:" + str(urgency) +
                       "&importance:" + str(importance) )
    
                       



