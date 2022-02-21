# Hemophilia Thingo v1.0
import random

# Constants
import copy


# TODO: Make this more random in the future. Doesn't seem worth the time currently.

number_of_bleeds = None
doses_on_hand = 0
# Don't really need this currently
# current_date = None
last_shipment = None
infusions = []
bleeds = []
bleeds_strings = []

days_as_str = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
months_as_str = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

prophey_schedule_main = [1, 3, 5]
non_prophey_bleeds = [0, 2, 4]
prophey_schedule_alt = [2, 4, 6]
current_schedule = None

bleed_locations = ['Elbow', 'Ankle', 'Calf', 'Finger']

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


def get_days_in_month(month):
    return months[month]


def get_wkday_str(wkday):
    return days_as_str[wkday]


def randomize_bleed_location():
    rand_index = random.randrange(len(bleed_locations))
    return bleed_locations[rand_index]


def randomize_bleed_severity():
    return random.randrange(2)


# Object used to create dates and tie them with information about the infusion performed on that date.
# TODO: This needs to be changed into multiple objects. Think inheritance.
class FullDate:
    def __init__(self, wkday, month, date, year, infusion_type, bleed_location, bleed_severity):
        self.wkday = wkday
        self.date = date
        self.month = month
        self.year = year
        self.infusion_type = infusion_type
        self.bleed_location = bleed_location
        self.bleed_severity = bleed_severity
        self.str_date = None

    def make_str_date(self):
        d = str(self.date)
        m = str(self.month)
        y = str(self.year)
        self.str_date = m + d + y

    # I can put the conditional statement inside f string
    def print_date(self):
        if self.infusion_type == 'Prophey':
            print(f'{get_wkday_str(self.wkday)} - {self.month}/{self.date}/{self.year} - {self.infusion_type}')
        else:
            print(f'{get_wkday_str(self.wkday)} - {self.month}/{self.date}/{self.year} - {self.bleed_location} {self.infusion_type}')


def update_wkday(days, wkday):
    leftover = days % 7
    if leftover + wkday > 6:
        new_wkday = leftover + (wkday - 7)
    else:
        new_wkday = leftover + wkday
    return new_wkday


def add_days(days, date):
    date_copy = copy.deepcopy(date)
    date_copy.wkday = update_wkday(days, date_copy.wkday)
    date_copy.date += days
    while date_copy.date > get_days_in_month(date_copy.month):
        date_copy.date -= get_days_in_month(date_copy.month)
        date_copy.month += 1
        if date_copy.month > 12:
            date_copy.year += 1
            date_copy.month = 1
    date_copy.make_str_date()
    return date_copy


def make_bleeds(date):
    while len(bleeds) < number_of_bleeds:
        date_copy = copy.deepcopy(date)
        if date_copy.wkday in [6, 0, 1, 2, 3]:
            bleed_range = random.randrange(1, 24)
        elif date_copy.wkday in [4, 5]:
            bleed_range = random.randrange(1, 25)
        else:
            print('error creating bleeds, this only happened because I forgot to check input on date')
            break

        bleed = add_days(bleed_range, date)
        bleed.bleed_location = randomize_bleed_location()
        bleed.infusion_type = 'Bleed'

        if bleed.str_date not in bleeds_strings:
            serialize_bleed(bleed)


def serialize_bleed(bleed):
    bleeds.append(bleed)
    bleeds_strings.append(bleed.str_date)


def make_log(date, doses, schedule):
    while doses > 0:
        if date.wkday == 0 and date.str_date not in bleeds_strings:
            schedule = prophey_schedule_main
        if date.wkday in schedule and date.str_date not in bleeds_strings:
            doses -= 1
            infusion = copy.deepcopy(date)
            infusion.infusion_type = 'Prophey'
            infusions.append(infusion)
            date = add_days(1, date)
        elif date.str_date in bleeds_strings:
            doses -= 1
            bleed_index = bleeds_strings.index(date.str_date)
            bleed = bleeds[bleed_index]
            if bleed.wkday in non_prophey_bleeds:
                schedule = prophey_schedule_alt

            infusions.append(bleed)
            date = add_days(1, date)
        else:
            date = add_days(1, date)


def print_log():
    for infusion in infusions:
        infusion.print_date()


def randomoze_amount_bleeds():
    return random.randrange(2, 4)


if __name__ == '__main__':
    number_of_bleeds = randomoze_amount_bleeds()
    print(number_of_bleeds)
    # TODO: Come up with a better way to make str date on object creation.
    last_shipment = FullDate(1, 1, 31, 2022, None, None)
    last_shipment.make_str_date()
    doses_on_hand = 12
    current_schedule = prophey_schedule_main
    # TODO: Come up with a better way to make str date on object creation.
    # TODO: Add random 'side' for bleed. Can only be done manually currently.
    # TODO: But really I need to streamline the creation of objects, currently to prone to user error.0
    b1 = FullDate(3, 2, 2, 2022, 'Bleed', 'Left Elbow', 0)
    b2 = FullDate(4, 2, 10, 2022, 'Bleed', randomize_bleed_location(), 0)

    b1.make_str_date()
    b2.make_str_date()
    serialize_bleed(b1)
    serialize_bleed(b2)
    make_bleeds(last_shipment)
    print(bleeds_strings)
    make_log(last_shipment, doses_on_hand, current_schedule)
    print_log()
    # k.print_date()
    # add_days(5, k).print_date()
    # k.print_date()
    # k.make_str_date()
    # print(k.str_date)