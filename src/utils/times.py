from datetime import datetime as dt

def datetime_now():

    now = dt.now()
    year = now.year
    month = now.strftime('%m')
    day = now.strftime('%d')
    hour = now.strftime('%H')
    second = now.strftime('%S')
    now_str = "{}-{}-{}-{}-{}".format(year,month,day,hour,second)
    return now_str