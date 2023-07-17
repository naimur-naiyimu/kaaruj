import datetime
from datetime import timedelta
today = datetime.datetime.today()
today_date = datetime.date.today()
import calendar

def getNumberofDays():
    count = 6
    today =today_date
    while 1:
        my_date = today - timedelta(days=count)
        dayname = calendar.day_name[my_date.weekday()]
        if (dayname == 'Saturday'):
            break
        count -= 1

    return count


def getTodayDay(today):
    dayname = calendar.day_name[today.weekday()]
    return dayname

def todays_queryset(model_name):
    year = today.year
    month = today.month
    start_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                    hour=0, minute=0, second=0)  # represents 00:00:00
    end_date = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                  hour=23, minute=59, second=59)
    filtered_data = model_name.objects.filter(created_at__range=[start_date, end_date])
    return filtered_data

def weekly_queryset(model_name):
    today = today_date
    start_number = getNumberofDays()
    weeek_started = today - timedelta(days=start_number)
    todays_data = today + timedelta(days=1)  # so that it includes in the result
    filtered_data = model_name.objects.filter(created_at__range=[weeek_started, todays_data])
    delta = datetime. timedelta(days=1)
    return filtered_data


      



def monthly_queryset(model_name):
    today = datetime.datetime.now().date()
    year = today.year
    month = today.month
    start_date = datetime.date(year=year, month=month, day=1)
    last_day_of_month = 31 if month == 12 else (datetime.date(year, month+1, 1) - datetime.timedelta(days=1)).day
    end_date = datetime.datetime(year=year, month=month, day=last_day_of_month, hour=23, minute=59, second=59)
    filtered_data = model_name.objects.filter(updated_at__range=[start_date, end_date])
    return filtered_data

def yearly_queryset(model_name):
    today = today_date
    year = today.year
    start_date = datetime.datetime(year=today.year, month=1, day=1,
                                    hour=0, minute=0, second=0)  # represents 00:00:00
    end_date = datetime.datetime(year=today.year, month=12, day=31,
                                  hour=23, minute=59, second=59)
    filtered_data =model_name.objects.filter(created_at__range=[start_date, end_date])
    return filtered_data
