import calendarHelperFun as calhelp
import scheduler
import datetime

def basic_health_event():
    sch = scheduler.scheduler()
    sleep_week_event = calhelp.eventCreator(datetime.datetime(2019,1,13,23,30),
                                       datetime.datetime(2019,1,14,7,30),
                                        0,
                                        -999,
                                        'Helath',
                                        5,
                                        5,
                                        'Sleep',
                                        -120)
    
    sleep_week_event = calhelp.createRecurringEvent(sleep_week_event,'SU,MO,TU,WE,TH')
    sleep_week_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    shower_week_event = calhelp.eventCreator(datetime.datetime(2019,1,13,23,0),
                                       datetime.datetime(2019,1,13,23,25),
                                        0,
                                        -999,
                                        'Helath',
                                        5,
                                        5,
                                        'Shower',
                                        -120)
    
    shower_week_event = calhelp.createRecurringEvent(shower_week_event,'SU,MO,TU,WE,TH')
    shower_week_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    calhelp.updateEvent(sch.service,shower_week_event)
    
    brkfst_week_event = calhelp.eventCreator(datetime.datetime(2019,1,14,7,35),
                                       datetime.datetime(2019,1,14,8,00),
                                        0,
                                        -999,
                                        'Helath',
                                        5,
                                        5,
                                        'Breakfast',
                                        -120) 
    brkfst_week_event = calhelp.createRecurringEvent(brkfst_week_event,'MO,TU,WE,TH,FR')
    brkfst_week_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    calhelp.updateEvent(sch.service,brkfst_week_event)
    
    sleep_weekend_event = calhelp.eventCreator(datetime.datetime(2019,1,18,23,30),
                                       datetime.datetime(2019,1,19,8,30),
                                        0,
                                        -999,
                                        'Helath',
                                        5,
                                        5,
                                        'Sleep',
                                        -120)
    
    sleep_weekend_event = calhelp.createRecurringEvent(sleep_weekend_event,'FR,SA')
    sleep_weekend_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    calhelp.updateEvent(sch.service,sleep_weekend_event)
    
    shower_weekend_event = calhelp.eventCreator(datetime.datetime(2019,1,18,23,0),
                                       datetime.datetime(2019,1,18,23,25,0),
                                        0,
                                        -999,
                                        'Helath',
                                        5,
                                        5,
                                        'Shower',
                                        -120)
    
    shower_weekend_event = calhelp.createRecurringEvent(shower_weekend_event,'FR,SA')
    shower_weekend_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    calhelp.updateEvent(sch.service,shower_weekend_event)
    
    brkfst_weekend_event = calhelp.eventCreator(datetime.datetime(2019,1,19,8,35),
                                       datetime.datetime(2019,1,19,9,00),
                                        0,
                                        -999,
                                        'Helath',
                                        5,
                                        5,
                                        'Breakfast',
                                        -120) 
    brkfst_weekend_event = calhelp.createRecurringEvent(brkfst_weekend_event,'SA,SU')
    brkfst_weekend_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    calhelp.updateEvent(sch.service,brkfst_weekend_event)
    
    dinner_event = calhelp.eventCreator(datetime.datetime(2019,1,13,17,30),
                                       datetime.datetime(2019,1,13,19,00),
                                        0,
                                        -999,
                                        'Health',
                                        5,
                                        4,
                                        'Dinner',
                                        -120) 
    dinner_event = calhelp.createRecurringEvent(dinner_event,'MO,TU,WE,TH,FR,SA,SU')
    dinner_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    calhelp.updateEvent(sch.service,dinner_event)
    
    
def createStudyTemplates():
    sch =scheduler.scheduler()
    ECE_240 = sch.newEventTemplate(event_name = 'ECE 240 Study',
                                   event_type = 'Basic Study',
                                   calendar = calhelp.getCalendarId(sch.service,'Study'),
                                   duration = 120,
                                   days_till_expire = 0,
                                   urgency = 5,
                                   importance = 4,
                                   reschedulability = 1,
                                   extensibility = 30,
                                   shortenability = 0)
    ECE_250 = sch.newEventTemplate(event_name = 'ECE 250 Study',
                                   event_type = 'Basic Study',
                                   calendar = calhelp.getCalendarId(sch.service,'Study'),
                                   duration = 60,
                                   days_till_expire = 0,
                                   urgency = 5,
                                   importance = 4,
                                   reschedulability = 1,
                                   extensibility = 30,
                                   shortenability = 0)
    ECE_222 = sch.newEventTemplate(event_name = 'ECE 222 Study',
                                   event_type = 'Basic Study',
                                   calendar = calhelp.getCalendarId(sch.service,'Study'),
                                   duration = 60,
                                   days_till_expire = 0,
                                   urgency = 5,
                                   importance = 4,
                                   reschedulability = 1,
                                   extensibility = 30,
                                   shortenability = 0)
    ECE_290 = sch.newEventTemplate(event_name = 'ECE 290 Study',
                                   event_type = 'Basic Study',
                                   calendar = calhelp.getCalendarId(sch.service,'Study'),
                                   duration = 60,
                                   days_till_expire = 0,
                                   urgency = 5,
                                   importance = 4,
                                   reschedulability = 1,
                                   extensibility = 30,
                                   shortenability = 0)
    
    sch.saveEventTemplate(ECE_240,'ECE_240_Study')
    sch.saveEventTemplate(ECE_250,'ECE_250_Study')
    sch.saveEventTemplate(ECE_222,'ECE_222_Study')
    sch.saveEventTemplate(ECE_290,'ECE_290_Study')
def createDownTimeTemplate():
    sch = scheduler.scheduler()
    Down_Time = sch.newEventTemplate(event_name = 'Down Time',
                               event_type = 'Free Time',
                               calendar = calhelp.getCalendarId(sch.service,'Health'),
                               duration = 60,
                               days_till_expire = 0,
                               urgency = 1,
                               importance = 1,
                               reschedulability = -1, #-1 is a special reschedulability class meaning fine to drop (with no consequences)
                               extensibility = 30,
                               shortenability = 60)
    sch.saveEventTemplate(Down_Time,'Down_Time')
    
if __name__ == '__main__':
    #basic_study()
    sch = scheduler.scheduler()
    createStudyTemplates()
    createDownTimeTemplate()
    ECE240 = sch.loadEventTemplate('ECE_240_Study')
    ECE250 = sch.loadEventTemplate('ECE_250_Study')
    ECE222 = sch.loadEventTemplate('ECE_222_Study')
    ECE290 = sch.loadEventTemplate('ECE_290_Study')
    
    Down_Time = sch.loadEventTemplate('Down_Time')
    
    start_date = datetime.date(2019,1,28)
    end_date = datetime.date(2019,2,1)
    
    sch.scheduleDailyEvent(Down_Time,by_daily = True,
                           by_daily_interval = 0,
                           period_start_date = start_date,
                           period_end_date = end_date,
                           default_start_time = datetime.time(22,0))
    
    sch.scheduleDailyEvent(ECE240,by_daily = True,
                           by_daily_interval = 0,
                           period_start_date = start_date,
                           period_end_date = end_date)
    sch.scheduleDailyEvent(ECE290,by_week = True,
                           by_week_day = 'TU,TH',
                           period_start_date = start_date,
                           period_end_date = end_date)
    sch.scheduleDailyEvent(ECE250,by_daily = True,
                           by_daily_interval = 0,
                           period_start_date = start_date,
                           period_end_date = end_date)
    sch.scheduleDailyEvent(ECE222,by_daily = True,
                           by_daily_interval = 0,
                           period_start_date = start_date,
                           period_end_date = end_date)