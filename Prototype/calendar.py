import calendarHelperFun as calhelp
import scheduler
import datetime

def main():
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
                                        5,
                                        'Dinner',
                                        -120) 
    dinner_event = calhelp.createRecurringEvent(dinner_event,'MO,TU,WE,TH,FR,SA,SU')
    dinner_event['cal_id'] = calhelp.getCalendarId(sch.service,'Health')
    
    calhelp.updateEvent(sch.service,dinner_event)
    
    
if __name__ == '__main__':
    main()