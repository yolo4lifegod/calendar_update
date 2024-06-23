from flask import Flask
from config import Config
from models import db
from calendar_app import calendar_bp
from dotenv import load_dotenv
import os
from datetime import datetime
from models import User, Event
import time

load_dotenv()  # Load environment variables from .env file

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(calendar_bp, url_prefix='/calendar')

    return app

from flask import Blueprint, render_template, request, Response
from models import db, User, Event
from icalendar import Calendar, Event as ICalEvent
from datetime import datetime

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/')
def index():
    return render_template('index.html')

@calendar_bp.route('/feed/<int:user_id>.ics')
def ical_feed(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    cal = Calendar()
    cal.add('prodid', '-//Your Organization//Your Calendar Product//EN')
    cal.add('version', '2.0')
    
    for event in user.events:
        cal_event = ICalEvent()
        cal_event.add('summary', event.title)
        cal_event.add('dtstart', event.start_time)
        cal_event.add('dtend', event.end_time)
        cal_event.add('dtstamp', datetime.now())
        cal_event['uid'] = f'{event.id}@yourdomain.com'
        cal.add_component(cal_event)

    ical_content = cal.to_ical()

    response = Response(ical_content)
    response.headers['Content-Type'] = 'text/calendar'
    response.headers['Content-Disposition'] = f'attachment; filename={user.username}.ics'
    return response

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        # Add sample data for testing
        db.drop_all()
        db.create_all()

        user = User(username='john_doe', email='john@example.com')
        db.session.add(user)
        db.session.commit()

        event1 = Event(title='Math Class', start_time=datetime(2024, 9, 1, 9, 0), end_time=datetime(2024, 9, 1, 10, 0), user_id=user.id)
        event2 = Event(title='Physics Class', start_time=datetime(2024, 9, 1, 11, 0), end_time=datetime(2024, 9, 1, 12, 0), user_id=user.id)
        db.session.add(event1)
        db.session.add(event2)
        db.session.commit()

        #time.sleep(3600)

        #event3 = Event(title='Lang` Class', start_time=datetime(2024, 9, 1, 13, 0), end_time=datetime(2024, 9, 1, 14, 0), user_id=user.id)
        #db.session.add(event3)
        #db.session.commit()

    app.run(debug=True)
