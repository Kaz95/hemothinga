# Hemophilia Thingo v1.0
import random

# Constants
import copy

number_of_bleeds = 2
doses_on_hand = 0
# Don't really need this currently
# current_date = None
last_shipment = None
infusions = []
bleeds = []
bleeds_strings = []

days_as_str = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
months_as_str = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

prophey_schedule = [1, 3, 5]


months = {
        1: 31,
        2: 28,
        3: 31,
        4: 30,
        5: 31,
        6: 30,
        7: 31,
        8: 31,
        9: 30,
        10: 31,
        11: 30,
        12: 31
        }


def new_shipment(cur_date):
    last_ship = cur_date
    return last_ship, 12


def get_days_in_month(month):
    return months[month]


def get_wkday_str(wkday):
    return days_as_str[wkday]


# Object used to create dates and tie them with information about the infusion performed on that date.
class FullDate:
    def __init__(self, wk_day, month, date, year, infusion_type):
        self.wk_day = wk_day
        self.date = date
        self.month = month
        self.year = year
        self.infusion_type = infusion_type
        self.str_date = None

    def make_str_date(self):
        d = str(self.date)
        m = str(self.month)
        y = str(self.year)
        self.str_date = m + d + y

    def print_date(self):
        print(f'{get_wkday_str(self.wk_day)} - {self.month}/{self.date}/{self.year}')


def update_wkday(days, wkday):
    leftover = days % 7
    if leftover + wkday > 6:
        new_wkday = leftover + (wkday - 7)
    else:
        new_wkday = leftover + wkday
    return new_wkday


def add_days(days, date):
    date_copy = copy.deepcopy(date)
    date_copy.wk_day = update_wkday(days, date_copy.wk_day)
    date_copy.date += days
    while date_copy.date > get_days_in_month(date_copy.month):
        date_copy.date -= get_days_in_month(date_copy.month)
        date_copy.month += 1
        if date_copy.month > 12:
            date_copy.year += 1
            date_copy.month = 1

    return date_copy


def make_bleed(date):
    date_copy = copy.deepcopy(date)
    if date.wk_day in [6, 0, 1, 2, 3]:
        bleed_range = random.randrange(1, 24)
        bleed = add_days(bleed_range, date_copy)
        bleed.infusion_type = 'Bleed'
        bleed.make_str_date()
        return bleed
    if date.wk_day in [4, 5]:
        bleed_range = random.randrange(1, 25)
        bleed = add_days(bleed_range, date_copy)
        bleed.infusion_type = 'Bleed'
        bleed.make_str_date()
        return bleed


def serialize_bleed(bleed):
    bleeds.append(bleed)
    bleeds_strings.append(bleed.str_date)


if __name__ == '__main__':
    last_shipment = FullDate(1, 1, 31, 2022, None)
    doses_on_hand = 12

    # k.print_date()
    # add_days(5, k).print_date()
    # k.print_date()
    # k.make_str_date()
    # print(k.str_date)