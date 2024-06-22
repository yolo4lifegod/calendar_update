from flask import Blueprint, render_template, request, Response
from models import db, User, Event
from icalendar import Calendar, Event as ICalEvent
from datetime import datetime

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/')
def index():
    return render_template('index.html')

@calendar_bp.route('/feed/<int:user_id>')
def ical_feed(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    cal = Calendar()
    for event in user.events:
        cal_event = ICalEvent()
        cal_event.add('summary', event.title)
        cal_event.add('dtstart', event.start_time)
        cal_event.add('dtend', event.end_time)
        cal_event.add('dtstamp', datetime.utcnow())
        cal_event['uid'] = f'{event.id}@yourdomain.com'
        cal_event.add('priority', 5)
        cal.add_component(cal_event)

    response = Response(cal.to_ical(), mimetype='text/calendar')
    response.headers['Content-Disposition'] = f'attachment; filename={user.username}.ics'
    return response