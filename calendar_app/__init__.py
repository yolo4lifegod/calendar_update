from flask import Blueprint

# Create a blueprint named 'calendar'
calendar_bp = Blueprint('calendar', __name__)

# Import routes so they are registered with the blueprint
from . import routes