# AutomaticChouseisan

Automatically creates a chouseisan using Splinter.  Currently adds all weekdays (not including Japanese holidays) between today and 20 days from today.

By default, it does not submit the form, allowing the user to set the title/comment/adjust the dates.  It can be adjusted to auto submit by removing the second parameter in the call to `makeChouseisan`.

TODO:
* Take command line arguments for title/comment/day/duration
* Make holiday checking more efficient
* Consider using `requests` and simply returning the url
