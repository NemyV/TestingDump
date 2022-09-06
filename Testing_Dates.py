from datetime import datetime, timedelta
from kivy.config import ConfigParser
import time
configparser = ConfigParser()
configparser.read("sample.ini")
# x = datetime.now()
# y = datetime.now()
y = datetime(2022, 7, 8)
# x = datetime(2022, 1, 4) # this is Thursday and week 1 in ISO calendar; should be 1 in custom calendar w/ week starting Thu
# y = datetime(2020, 1, 3) # this is Friday and week 1 in ISO calendar; should be 2 in custom calendar
# print(x)
# print(y)

def weeknum(dt):
    return dt.isocalendar()[1]

def myweeknum(dt):
    offsetdt = dt + timedelta(days=2);  # you add 3 days to Mon to get to Thu
    return weeknum(offsetdt);

# print(weeknum(x));
# print(myweeknum(x));

# print(weeknum(y));
# print(myweeknum(y));


def calculate_week_day(date_for_calculation):
    offsetdt = date_for_calculation + timedelta(days=2);  # days= 2 days to Mon to get to Wen

    last_date = datetime.fromisoformat(configparser.get('Date', 'Last_date'))
    current_date = datetime.now()
    print(current_date)
    delta = current_date - last_date

    configparser.set('Date', 'Last_date', last_date)

    current_week = weeknum(offsetdt)
    last_week = configparser.get('Date', 'Last_week')
    print(current_week, last_week)
    if current_week > int(last_week):
        # INSERT THINGS TO DO HERE
        # Accept weeklies ...
        print("Last week LARGER than this week")
        configparser.set('Date', 'Last_week', weeknum(offsetdt))
        configparser.write()
    print(delta.days)
    # if current_week> last_checked_week:
    #     # And accept all weekly quests again
    #     current_week = last_checked_week
    #
    # if current_day > current_day:
    #     # And accept all daily quests again
    #     current_day = current_day
    # if charx == finished_daily :
    #     save_date
    return weeknum(offsetdt);

calculate_week_day(y)