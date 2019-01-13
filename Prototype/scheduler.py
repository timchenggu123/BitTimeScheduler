import calendarHelperFun as calhelp
import connection
import datetime

class scheduler():
    
    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/calendar'
        self.service = connection.googleCalendar(self.SCOPES)
        self.bucket_list = list()
        
    def addBucketList(self,event,calendar_id):
        event['cal_id'] = calendar_id
        self.bucket_list.append(event)
        
    def showBucketList(self):
        if self.bucket_list:
            for event in self.bucket_list:
                print(event['start']['dateTime'] + ' ' + event['summary'])
    
    def scheduleBucketList(self):
        if self.bucket_list:
            for event in self.bucket_list:
                print('Scheduling event:' + event['summary'] + '.....')
                start_datetime = calhelp.str2time(event['start']['dateTime'])
                custom_tags = calhelp.getCustomTags(event)
                days_till_expire = custom_tags['days_till_expire']
                success = self.rescheduler(event,start_datetime,days_till_expire)
                if success:
                    print(event['summary'] + ' has been scheduled successfully!')
                    print()
                else:
                    print(event['summary'] + ' cannot be scheduled')
        else:
            print('bucket list is empty !')
        
    def rescheduler(self,target_event,start_datetime,for_ndays):
        '''needs work'''
        cal_presets = self.getCalPresets()
        all_events = calhelp.getAllEvents(self.service,start_datetime,for_ndays, cal_presets) #
        free_time = calhelp.getFreeTime(self.service,start_datetime,for_ndays)
        
        all_events = all_events + free_time
        all_events = sorted(all_events,key = lambda s: s['start']['dateTime'])
        
        reschedulability = -1
        print('searching at reschedulability level: -1')
        filtered_events = self.reschedulabilityFilter(all_events,reschedulability)
        
        target_event_duration = calhelp.getEventDuration(target_event)
        filtered_events = self.timeFitFilter(filtered_events,target_event_duration)
        
        if len(filtered_events) >= 0:
            ranked_events = self.ranker(filtered_events,target_event)
            
            if self.rankingVerifier(ranked_events):
                to_be_updated = ranked_events[0]
                new_start = to_be_updated['start']['dateTime']
                target_event_duration = calhelp.getEventDuration(target_event)
                new_end = calhelp.str2time(new_start) + datetime.timedelta(minutes = target_event_duration)
                new_end = calhelp.time2str(new_end)
                
                target_event['start']['dateTime'] = new_start
                target_event['end']['dateTime'] = new_end
                calhelp.updateEvent(self.service,target_event)
                
                return 1
                
        reschedulability = 1
        filtered_events = self.reschedulabilityFilter(all_events,reschedulability)
        
        target_event_duration = calhelp.getEventDuration(target_event)
        filtered_events = self.timeFitFilter(filtered_events,target_event_duration)
        
        if len(filtered_events) >= 0:
            ranked_events = self.ranker(filtered_events,target_event)
            
            if self.rankingVerifier(ranked_events):
                new_target_event = ranked_events[0]
                new_start_datetime = calhelp.str2time(new_target_event['end']['dateTime'])

                days_lapsed = new_start_datetime.date() - start_datetime.date()
                days_lapsed = days_lapsed.day
                new_for_ndays = for_ndays - days_lapsed
                
                success = self.rescheduler(new_target_event,new_start_datetime,new_for_ndays)
                
                if success:
                    to_be_updated = ranked_events[0]
                    new_start = to_be_updated['start']['dateTime']
                    target_event_duration = calhelp.getEventDuration(target_event)
                    new_end = calhelp.str2time(new_start) + datetime.timedelta(minutes = target_event_duration)
                    new_end = calhelp.time2str(new_end)
                    
                    target_event['start']['dateTime'] = new_start
                    target_event['end']['dateTime'] = new_end
                    calhelp.updateEvent(self.service,target_event)
                
                    return 1
                    
            
        #extensibility = target_event_duration
        #filtered_events = self.extensibilityFilter(all_events,extensibility)
        #Extensibility section to be worked on
        
        
        reschedulability = 0
        filtered_events = self.reschedulabilityFilter(all_events,reschedulability)
        
        target_event_duration = calhelp.getEventDuration(target_event)
        filtered_events = self.timeFitFilter(filtered_events,target_event_duration)
        
        ranked_events = self.ranker(filtered_events,target_event)
        
        if len(filtered_events) >= 0:
            ranked_events = self.ranker(filtered_events,target_event)
            
            if self.rankingVerifier(ranked_events,min_IU_score = 2):
                dropping_event = ranked_events[0]

                calhelp.dropEvent(self.service,dropping_event)

                new_start = dropping_event['start']['dateTime']
                target_event_duration = calhelp.getEventDuration(target_event)
                new_end = calhelp.str2time(new_start) + datetime.timedelta(minutes = target_event_duration)
                new_end = calhelp.time2str(new_end)
                
                target_event['start']['dateTime'] = new_start
                target_event['end']['dateTime'] = new_end
                calhelp.updateEvent(self.service,target_event)
                
                return 1
            
        print('failed to schedule event')
        return 0
            
    def getCalPresets(self):
        '''this is but a temporary solution. Idealistically this function is 
        supposed to retrieve preset information from json files'''
        
        presets = list()
        preset = {'cal_id' : 't4p9h18kn9ka3nf8sf6teobfbfouoo6t@import.calendar.google.com',
                  'description':("&reschedulability:" + str(0) +
                       "&expirary_date:" + str(-999) +
                       "&days_till_expire:" + str(0) +
                       "&event_type:" + 'School' +
                       "&urgency:" + str(5) +
                       "&importance:" + str(5) +
                       "&extensibility:" + str(0))
                  }
        presets.append(preset)

        return presets
    
    def rankingVerifier(self,ranked_events,min_IU_score = 0):
        print('candidate found, veryfying requirements.')
        if len(ranked_events) == 0 or ranked_events[0]['IUScore'] <= min_IU_score:
            print('fail:candidate did not meet requirement.')
            return False
        
        print('success: requirement met')
        return True 
    
    def extensibilityFilter(self,all_events,extensibility):
        remove_list = list()
        for event in all_events :
            custom_tag = calhelp.getCustomTags(event)
            if custom_tag['extensibility'] < 0 and custom_tag['extensibility'] < extensibility :\
                remove_list.append(event)
                
        for event in remove_list:
            all_events.remove(event)
        
        return all_events
    
    def reschedulabilityFilter(self,all_events,reschedulability):
        reschedulability = str(reschedulability)
        remove_list = list()
        for event in all_events:
            custom_tag = calhelp.getCustomTags(event)
            if not custom_tag['reschedulability'] == reschedulability:
                remove_list.append(event)
        for event in remove_list:
            all_events.remove(event)
            
        return all_events
    
    def timeFitFilter(self,all_events,duration):
        remove_list = list()
        for event in all_events:
            event_duration = calhelp.getEventDuration(event)
            if event_duration < duration:
                remove_list.append(event)
        for event in remove_list:
            all_events.remove(event)
                
        return all_events
    
    def ranker(self,events,target_event):
        print('ranking candidates...')
        target_duration = calhelp.getEventDuration(target_event)
        events = self.timeFitRanker(events,target_duration)
        events = self.IUScaleRanker(events,target_event)
        events = self.timeLagRanker(events,target_event)
        
        for event in events:
            event_total_score = event['time_fit_score'] + event['IUScore'] + event['time_lag_score']
            event['score'] = event_total_score
            
        events = sorted(events,key = lambda s: s['score'], reverse = True)
        
        return events
    
    def timeLagRanker(self,events,target_event,weight = 1):
        '''This ranks events slots by calculating how far back the event has 
        been pushed into future. Ideally, we want the event to take place as
        early as possible'''
        
        target_expire_days = calhelp.calcEventExpireDays(target_event)
        custom_tags = calhelp.getCustomTags(target_event)
        urgency = int(custom_tags['urgency'])
        today = datetime.date.today()
        upper_bound = today
        lower_bound = today + datetime.timedelta(days = int(target_expire_days/(urgency+1)))
        scoring_period = lower_bound - upper_bound
        scoring_period = scoring_period.days
        
        for event in events:
            event_start_date = calhelp.str2time(event['start']['dateTime']).date()
            from_lower_bound = lower_bound - event_start_date
            from_lower_bound = from_lower_bound.days
            if scoring_period == 0:
                if from_lower_bound == 0:
                    time_lag_score = 1
                else:
                    time_lag_score = 0
            else:
                if from_lower_bound <= 0:
                    time_lag_score = 0
                else:
                    time_lag_score = weight * from_lower_bound/scoring_period
            
            event['time_lag_score'] = time_lag_score
        
        return events
    
    def timeFitRanker(self,events,duration):
        '''This ranks how well the event fits the given slot'''
        
        for event in events:
            event_duration = calhelp.getEventDuration(event)
            time_fit_score = self.timeFitScoreCalculator(event_duration,duration)
            event['time_fit_score'] = time_fit_score
            
        return events
    
    def timeFitScoreCalculator(self,event_duration,duration,small_enough = 10,weight = 1):
        duration_difference = event_duration - duration
        
        if duration_difference == 0:
            duration_difference = 0.000001
        duration_difference_score = duration/duration_difference
        if duration_difference_score > 1:
            duration_difference_score =1
        duration_difference_score = round(duration_difference_score,1)
        duration_difference_score = duration_difference_score/10
        
        time_fit_remainder = divmod(event_duration,duration)[1]
        if time_fit_remainder < small_enough:
            time_fit_score = weight - 0.1
        else:
            time_fit_score = round((1- (time_fit_remainder/duration)) *weight,1)
            
        time_fit_score += duration_difference_score
        
        return time_fit_score
    
    def IUScaleRanker(self,events,target_event):
        target_custom_tags = calhelp.getCustomTags(target_event)
        importance = target_custom_tags['importance']
        urgency = target_custom_tags['urgency']
        
        for event in events:
            event_custom_tags = calhelp.getCustomTags(event)
            event_importance = event_custom_tags['importance']
            event_urgency = event_custom_tags['urgency']
            
            event_IUScore = int(importance) + int(urgency) - (int(event_importance) + int(event_urgency))
            
            event['IUScore'] = event_IUScore
            
        return events

#test
sch = scheduler()
start = datetime.datetime.now() + datetime.timedelta(minutes = 60)
end = datetime.datetime.now() + datetime.timedelta(minutes = 120)
event1 = calhelp.eventCreator(start,end,0,0,'Health',0,5,'test',0,15)
calid = calhelp.getCalendarId(sch.service,'Health')
sch.addBucketList(event1,calid)
sch.showBucketList()
sch.scheduleBucketList()
            
    