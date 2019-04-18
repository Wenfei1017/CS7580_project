from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from eventmanager import db, login_manager
from eventmanager.registrations.model import Registration
from flask_sqlalchemy import SQLAlchemy
import enum


def load_event(event_id):
    return Event.query.get(event_id)


class EventEnum(enum.Enum):
    pets = 'pets'
    beauty = 'beauty'
    outside = 'outside'
    sports = 'sports'
    coffee = 'coffee'
    beer_and_wine = 'beer and wine'
    reading = 'reading'
    others = 'others'


class StatusEnum(enum.Enum):
    Starting_soon = 'starting soon'
    Finished = 'finished'
    Opening_now = 'opening now'


class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    time_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    time_start = db.Column(db.DateTime, nullable=True)
    time_end = db.Column(db.DateTime, nullable=True)
    event_address = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category = db.Column(db.Enum(EventEnum), nullable=False)

    status = db.Column(db.Enum(StatusEnum), nullable=True)
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade="all, delete-orphan")


    def __repr__(self):
        return f"Event('{self.id}', '{self.title}', '{self.description}', '{self.category}', \
        '{self.time_start}', '{self.time_end }')"
