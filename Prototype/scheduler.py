import calendarHelperFun as calhelp
import connection
import datetime

class scheduler():
    
    def __init__(self):
        self.SCOPES = 'https://www.googleapis.com/auth/calendar'
        self.service = connection.googleCalendar(self.SCOPES)
        
    def rescheduler(self,target_event,start_datetime,for_ndays):
        '''needs work'''
        all_events = calhelp.getAllEvents(self.service,start_date,for_ndays) #
        
        reschedulability = -1
        filtered_events = self.reschedulabilityFilter(all_events,reschedulability)
        
        target_event_duration = calhelp.getEventDuration(target_event)
        filtered_events = self.timeFitFilter(self,filtered_events,target_event_duration)
        
        if len(filtered_events) >= 0
            ranked_events = self.ranker(filtered_events,target_event)
            
            if self.rankingVerifier(ranked_events):
                to_be_updated = ranked_events[0]
                new_start = to_be_updated['start']['dateTime']
                new_end = to_be_updated['end']['dateTime']
                target_event['start']['dateTime'] = new_start
                target_event['end']['dateTime'] = new_end
                calhelp.updateEvent(self.service,target_Event)
                
                return 1
                
        reschedulability = 1
        filtered_events = self.reschedulabilityFilter(all_events,reschedulability)
        
        target_event_duration = calhelp.getEventDuration(target_event)
        filtered_events = self.timeFitFilter(self,filtered_events,target_event_duration)
        
        if len(filtered_events) >= 0
            ranked_events = self.ranker(filtered_events,target_event)
            
            if self.rankingVerifier(ranked_events):
                new_target_event = ranked_events[0]
                new_start_datetime = calhelp.str2time(new_target_event['end']['dateTime'])
                new_custom_tags = calhelp.getCustomTags(new_target_event)
                new_days_till_expire = new_custom_tags['days_till_expire']
                
                success = self.rescheduler(new_target_event,new_start_datetime,new_days_till_expire)
                
                if success:
                    to_be_updated = ranked_events[0]
                    new_start = to_be_updated['start']['dateTime']
                    new_end = to_be_updated['end']['dateTime']
                    target_event['start']['dateTime'] = new_start
                    target_event['end']['dateTime'] = new_end
                    calhelp.updateEvent(self.service,target_Event)
                
                    return 1
                    
            
        #extensibility = target_event_duration
        #filtered_events = self.extensibilityFilter(all_events,extensibility)
        #Extensibility section to be worked on
        
        
        reschedulability = 0
        filtered_events = self.reschedulabilityFilter(all_events,reschedulability)
        
        target_event_duration = calhelp.getEventDuration(target_event)
        filtered_events = self.timeFitFilter(self,filtered_events,target_event_duration)
        
        ranked_events = self.ranker(filtered_events,target_event)
        
        if len(filtered_events) >= 0
            ranked_events = self.ranker(filtered_events,target_event)
            
            if self.rankingVerifier(ranked_events,min_IU_score = 2):
                dropping_event = ranked_events[0]
                new_start_datetime = calhelp.str2time(new_target_event['end']['dateTime'])
                new_custom_tags = calhelp.getCustomTags(new_target_event)
                new_days_till_expire = new_custom_tags['days_till_expire']
                
                success = self.rescheduler(new_target_event,new_start_datetime,new_days_till_expire)
                
                if success:
                    to_be_updated = ranked_events[0]
                    new_start = to_be_updated['start']['dateTime']
                    new_end = to_be_updated['end']['dateTime']
                    target_event['start']['dateTime'] = new_start
                    target_event['end']['dateTime'] = new_end
                    calhelp.updateEvent(self.service,target_Event)
                
                    return 1
            
        print('failed to schedule event')
        return 0
            
    def rankingVerifier(self,ranked_events,min_IU_score = 0):

        if ranked_events[0]['IUScore'] <= min_IU_Score:
            return False
        
        return True
    
    def extensibilityFilter(self,all_events,extensibility):
        for event in all_events :
            custom_tag = calhelp.getCustomTags(event)
            if custom_tag['extensibility'] < 0 and cutom_tag['extensibility'] < extensibility :
                all_events.remove(event)
        
        return all_events
    
    def reschedulabilityFilter(self,all_events,reschedulability):
        for event in all_events:
            custom_tag = calhelp.getCustomTags(event)
            if not custom_tag['reschedulability'] == reschedulability:
                all_events.remove(event)
            
        return all_events
    
    def timeFitFilter(self,all_events,duration):
        for event in all_events:
            event_duration = calhelp.getEventDuration(event)
            if event_duration < duration:
                all_events.remove(event)
                
        return all_events
    
    def ranker(self,events,target_event):
        target_duration = calhelp.getEventDuration(target_event)
        events = self.timeFitRanker(events,target_duration)
        events = self.IUScaleRanker(events,target_event)
        
        for event in events:
            event_total_score = event['time_fit_score'] + event['IUScore']
            event['score'] = event_total_score
            
        events = sorted(events,key = lambda s: s['score'])
        
        return events
        
    def timeFitRanker(self,events,duration):
        
        for event in events:
            event_duration = calhelp.getEventDuration(event)
            time_fit_score = self.timeFitScoreCalculator(event_duration,duration)
            event['time_fit_score'] = time_fit_score
            
        return events
            
    def timeFitScoreCalculator(event_duration,duration,small_enough = 10,weight = 2):
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
            
            event_IUScore = importance+urgency - (event_importance + event_urgency)
            
            event['IUScore'] = event_IUScore
            
        return events
            
            
    