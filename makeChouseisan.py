# -*- coding: utf-8 -*-
import sys
try:
    from splinter import Browser
except ImportError:
    print("Error, splinter not installed.  Install using pip install selenium&&pip install splinter&&brew install chromedriver")
    sys.exit(1)
try:
    import argparse
except ImportError:
    print("Unable to import argparse.  Try updating python or running with python3.")
    sys.exit(1)
import datetime
import time

jDays = [ur"月",
         ur"火",
         ur"水",
         ur"木",
         ur"金",
         ur"土",
         ur"日"]

autoSubmit = False

# ===== Holiday ====
API_KEY = 'AIzaSyCiD3By0rW9zsJGs9NVxTGJgVZykgnzJYQ' # chen_nicholas
CALENDAR_ID = 'ja.japanese#holiday@group.v.calendar.google.com'
HOLIDAYS_CACHE = 'holidays.txt'

def removeHolidays(days):
    # TODO: Make this more efficient
    holidays = [convertStringToDatetime(l) for l in parseFileToTwoDList(HOLIDAYS_CACHE)]
    for holiday in holidays:
        for day in days:
            if day.date() == holiday.date():
                days.remove(day)
    return days

def updateHolidayCache():
    # APIを叩く
    from apiclient.discovery import build
    service = build(serviceName='calendar', version='v3', developerKey=API_KEY)
    events = service.events().list(calendarId=CALENDAR_ID).execute()
    with open(HOLIDAYS_CACHE, 'w') as f:
        for item in sorted(events['items'], key=lambda item: item['start']['date']):
            f.write( u'{0}\t{1}'.format( item['start']['date'], item['summary'] ) )

# ===== Other date related =====
def isWeekday(day):
    return day.weekday() < 5

def getListOfDaysFrom(startDay, rng):
    ''' Gets all days starting from startDay for a length of rng days '''
    return [startDay + datetime.timedelta(days=n) for n in range(rng)]

def getWeekdays(startDay, rng):
    ''' Gets only the weekdays from startDay for a length of rng days '''
    return removeHolidays(filter(lambda x: isWeekday(x), getListOfDaysFrom(startDay, rng)))

def getWeekends(startDay, rng):
    ''' Gets only the weekends from startDay for a length of rng days '''
    return filter(lambda x: not isWeekday(x), getListOfDaysFrom(startDay, rng))

# ===== Chouseisan related =====
def formatDay(day, weekdayTime, weekendTime):
    ''' Format a day to be put into the web form '''
    return ur"%s/%s(%s) %s~" %(day.month, day.day, jDays[day.weekday()], weekdayTime if isWeekday(day) else weekendTime)

def makeChouseisan(listOfDays, weekdayTime, weekendTime, autosubmit=True):
    # TODO: add Title, Comment as arguments
    browser = Browser('chrome')
    browser.visit("https://chouseisan.com/schedule/newEvent/create")

    browser.find_by_id("name").fill("Title")
    browser.find_by_id("comment").fill("Comment")
    browser.find_by_id("kouho").fill("\n".join([formatDay(day, weekdayTime, weekendTime) for day in listOfDays]))

    if autosubmit:
        browser.find_by_id("createBtn").first.click()

    while len(browser.windows) > 0:
        time.sleep(10)

# ===== Helper =====
def parseFileToTwoDList(fp):
    with open(fp, 'r') as f:
        return [line.split() for line in f if not line.isspace()]

def convertStringToDatetime(s, delimiter="-"):
    date = s[0].split(delimiter)
    for num in date:
        if num[0] == "0":
            num = num[1:]
    return datetime.datetime(*map(lambda x: int(x), date))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-days", choices=["all", "weekday", "weekend"],
                        help="Which days to include",
                        default="all")
    parser.add_argument("-weekdaystart",
                        help="Time to start on weekdays",
                        default="20:00")
    parser.add_argument("-weekendstart",
                        help="Time to start on weekends",
                        default="18:00")
    parser.add_argument("-startday", "-start",
                        help="The day to start creating from",
                        default=datetime.datetime.now())
    parser.add_argument("-range",
                        help="How many days from startday to include",
                        default=20)

    args = parser.parse_args()
    print(args)

    if args.days == "all":
        makeChouseisan(getListOfDaysFrom(args.startday, args.range),
                       args.weekdaystart, args.weekendstart, autoSubmit)
    elif args.days == "weekday":
        makeChouseisan(getWeekdays(args.startday, args.range),
                       args.weekdaystart, args.weekendstart, autoSubmit)
    elif args.days == "weekend":
        makeChouseisan(getWeekends(args.startday, args.range),
                       args.weekdaystart, args.weekendstart, autoSubmit)

if __name__ == "__main__":
    main()
