import datetime

def number_to_date(n):
    if int(n[1]) > 3:
        return '{}th'.format(n)
    else:
        if int(n[0]) == 1:
            return '{}th'.format(n)
        else:
            if int(n[1]) == 1:
                return '{}st'.format(n)
            elif int(n[1]) == 2:
                return '{}nd'.format(n)
            elif int(n[1]) == 3:
                return '{}rd'.format(n)

def to_now():
    return {
        'before yesterday': -2,
        'yesterday': - 1,
        'today': 0,
        'now': 0,
        'tomorrow': 1,
        'after tomorrow': 2
    }

def tellDate(date): 
    result = datetime.datetime.now() + datetime.timedelta(days=to_now()[date]) 
    month = result.strftime('%b')
    date = number_to_date(result.strftime('%d'))
    day = result.strftime('%A')
    return 'The required day is {}, {} {}'.format(day, month, date)
  
  
def tellTime(): 
  
    time = str(datetime.datetime.now())
    hour = time[11:13] 
    minute = time[14:16] 
    return "The time is {} hours and {} minutes".format(hour, minute)