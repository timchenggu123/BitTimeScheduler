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
    
    calhelp.updateEvent(sch.service,sleep_week_event)
    
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
    

def basic_study():
    sch = scheduler.scheduler()
    ECE_240 = calhelp.eventCreator(datetime.datetime(2019,1,14,00,00,00),
                                   datetime.datetime(2019,1,14,2,00,00),
                                   1,
                                   datetime.date(2019,1,20),
                                   'Basic Study',
                                   5,
                                   4,
                                   'ECE 240 <general>'
                                   )
    ECE_240['cal_id'] = calhelp.getCalendarId(sch.service,'Study')
    
    sch.scheduleDailyEvent(ECE_240)
    
    ECE_250 = calhelp.eventCreator(datetime.datetime(2019,1,14,00,00,00),
                                   datetime.datetime(2019,1,14,1,00,00),
                                   1,
                                   datetime.date(2019,1,20),
                                   'Basic Study',
                                   5,
                                   4,
                                   'ECE 250 <general>'
                                   )
    ECE_250['cal_id'] = calhelp.getCalendarId(sch.service,'Study')
    sch.scheduleDailyEvent(ECE_250)
    
    ECE_222 = calhelp.eventCreator(datetime.datetime(2019,1,14,00,00,00),
                                   datetime.datetime(2019,1,14,1,00,00),
                                   1,
                                   datetime.date(2019,1,20),
                                   'Basic Study',
                                   5,
                                   4,
                                   'ECE 222 <general>'
                                   )
    ECE_222['cal_id'] = calhelp.getCalendarId(sch.service,'Study')
    sch.scheduleDailyEvent(ECE_222)

    ECE_290 = calhelp.eventCreator(datetime.datetime(2019,1,14,00,00,00),
                                   datetime.datetime(2019,1,14,1,00,00),
                                   1,
                                   datetime.date(2019,1,18),
                                   'Basic Study',
                                   5,
                                   4,
                                   'ECE 290 <general>'
                                   )
    ECE_290['cal_id'] = calhelp.getCalendarId(sch.service,'Study')
    sch.scheduleDailyEvent(ECE_290,by_daily = True, by_daily_interval = 1)
    
if __name__ == '__main__':
    basic_study()