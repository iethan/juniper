from datetime import datetime as dt

def datetime_now():
    now = dt.now()    
    return "-".join([now.year,
                    now.strftime('%m'),
                    now.strftime('%d'),
                    now.strftime('%H'),
                    now.strftime('%M')])