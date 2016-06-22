# AutomaticChouseisan

Automatically creates a chouseisan using Splinter.  Currently adds [all/weekdays/weekends] (not including Japanese holidays, for weekdays) between a given start date and a given number of days in the future.

By default, it does not submit the form, allowing the user to set the title/comment/adjust the dates.  It can be adjusted to auto submit by changing the constant at the top of the file.

    usage: makeChouseisan.py [-h] [-days {all,weekday,weekend}]
                             [-weekdaystart WEEKDAYSTART]
                             [-weekendstart WEEKENDSTART] [-startday STARTDAY]
                             [-range RANGE]
    
    optional arguments:
      -h, --help            show this help message and exit
      -days {all,weekday,weekend}
                            Which days to include
      -weekdaystart WEEKDAYSTART
                            Time to start on weekdays
      -weekendstart WEEKENDSTART
                            Time to start on weekends
      -startday STARTDAY, -start STARTDAY
                            The day to start creating from
      -range RANGE          How many days from startday to include

TODO:
* Take command line arguments for title/comment
* Make holiday checking more efficient
* Consider using `requests` and simply returning the url
