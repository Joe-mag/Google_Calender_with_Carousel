from flask import Flask

app = Flask(__name__, static_url_path='/static')

app.config['GOOGLE'] = dict(
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
)

from model import Model
from view import View

@app.route('/')
def calendar():
   zalando= Model.retrieve_calendar()
   pythonireland_cal = Model.retrieve_meetup_calendar('https://api.meetup.com/2/events?key=223d6b746653574929553373f66116&group_urlname=pythonireland&sign=true')
   DataScientistsIreland_cal = Model.retrieve_meetup_calendar('https://api.meetup.com/2/events?key=223d6b746653574929553373f66116&group_urlname=DataScientistsIreland&sign=true')
   PyLadiesDublin_cal = Model.retrieve_meetup_calendar('https://api.meetup.com/2/events?key=223d6b746653574929553373f66116&group_urlname=PyLadiesDublin&sign=true')
   Deep_Learning_Dublin_cal = Model.retrieve_meetup_calendar('https://api.meetup.com/2/events?key=223d6b746653574929553373f66116&group_urlname=Deep-Learning-Dublin&sign=true')
   calendars = [{'name': 'meetupDataScientistsIreland', 'id': 'Data Scientists Ireland', 'events': DataScientistsIreland_cal},
                {'name': 'Zalando', 'events': zalando},
                {'name': 'meetup_PyLadiesDublin', 'id': 'Py Ladies Dublin', 'events': PyLadiesDublin_cal},
                {'name': 'meetup_pythonireland', 'id': 'Python Ireland', 'events': pythonireland_cal},
                {'name': 'meetup_Deep_Learning_Dublin', 'id': 'Deep Learning Dublin', 'events': Deep_Learning_Dublin_cal}
                ]

#   with open('/tmp/calendar.json', 'w') as f:
#      import json
#      json.dump(calendars, f)

   return View.get_calendar(calendars)

# for meet up calendar

@app.route('/meetups/<name>')
def meetup_calendar(name):
   events=Model.retrieve_meetup_calendar('https://api.meetup.com/2/events?key=223d6b746653574929553373f66116&group_urlname=%s&sign=true' % name)
   if not events:
      return "Calendar not found"
   return View.get_meetup_calendar_json(events)

if __name__=="__main__":
   app.run(debug=True)
