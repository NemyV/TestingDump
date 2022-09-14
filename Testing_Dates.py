from datetime import datetime, timedelta
from kivy.config import ConfigParser
import time
configparser = ConfigParser()
configparser.read("sample.ini")
# x = datetime.now()
# y = datetime.now()
y = datetime(2022, 9, 14, 3)
# x = datetime(2022, 1, 4) # this is Thursday and week 1 in ISO calendar; should be 1 in custom calendar w/ week starting Thu
# y = datetime(2020, 1, 3) # this is Friday and week 1 in ISO calendar; should be 2 in custom calendar
# print(x)
# print(y)

def weeknum(dt):
    return dt.isocalendar()[1]

def myweeknum(dt):
    offsetdt = dt + timedelta(days=3);  # you add 3 days to Mon to get to Thu
    return weeknum(offsetdt);

# print(weeknum(x));
# print(myweeknum(x));

# print(weeknum(y));
# print(myweeknum(y));


def calculate_weekly(current_character):
    current_date = datetime.now()
    set_date = datetime(2022, 8, 3, 12, 0, 0)  # Setting hour and day of the week for weekly to calculate
    c = current_date - set_date
    current_week = int(c.days/7)
    # minutes = c.total_seconds() / 60
    # hours = minutes / 60
    # print("Number of days:", c.days)
    # print("Number of weeks:", int(hours/168)) # 7 days = 168 h
    try:
        last_week = configparser.get(current_character, 'Last_week')
    except:
        configparser.add_section(current_character)
        configparser.set(current_character, 'Last_week', current_week)
        last_week = configparser.get(current_character, 'Last_week')
        configparser.write()

    print(current_week, last_week)
    if current_week > int(last_week):
        # INSERT THINGS TO DO HERE
        # Accept weeklies ...
        print("Accepting weeklies")
        configparser.set(current_character, 'Last_week', current_week)
        configparser.write()


def calculate_week_day(date_for_calculation, current_character):
    offsetdt = date_for_calculation + timedelta(hours=12);  # days= 2 days to Mon to get to Wen
    last_date = datetime.fromisoformat(configparser.get('Date', 'Last_date'))
    current_date = datetime.now()
    print(date_for_calculation)
    print(current_date)
    delta = current_date - last_date
    dt = datetime.now()
    print(dt.strftime('%A'))
    print(offsetdt.strftime('%A'))
    configparser.set('Date', 'Last_date', last_date)

    current_week = weeknum(offsetdt)
    last_week = configparser.get(current_character, 'Last_week')
    print(current_week, last_week)
    if current_week > int(last_week):
        # INSERT THINGS TO DO HERE
        # Accept weeklies ...
        print("Last week LARGER than this week")
        configparser.set(current_character, 'Last_week', weeknum(offsetdt))
        configparser.write()
    print("Same week")
    print(delta.total_seconds())
    print(int(13/7)) # Using int rounds down number to a lower value
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


# calculate_week_day(y, "Ggbard")

calculate_weekly("Gggungsdg ")
