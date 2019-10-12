from flask import Flask

from pi_info.blueprints.Weekday import Weekday


class Filters(object):
    def init_filters(self, app):
        @app.template_filter('formatdatetime')
        def format_datetime(value, format="%d %b %Y %I:%M %p"):
            """Format a date time to (Default): d Mon YYYY HH:MM P"""
            if value is None:
                return "-"
            return value.strftime(format)

        @app.template_filter('toWeekday')
        def to_weekday(value):
            if value is None:
                return "-"
            try:
                days = value.split(',')
                if len(days) == len(Weekday):
                    return 'Everyday'
                if len(days) == 5 and all(str(d) in days for d in range(1, 6)):
                    return 'Weekdays'
                if len(days) == 2 and all(str(d) in days for d in range(6, 8)):
                    return 'Weekends'
                return ", ".join([Weekday(int(day)).name for day in days])
            except:
                return value
