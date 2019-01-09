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