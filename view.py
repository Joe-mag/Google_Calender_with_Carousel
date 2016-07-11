from flask import render_template
# import json


class View(object):
    @classmethod
    def get_calendar(self, calendars):
        return render_template("base.html", calendars=calendars)

    @classmethod
    def get_meetup_calendar_json(self, events):
        return render_template("meetups_calendar.html", events=events)