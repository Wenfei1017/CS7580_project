from sqlalchemy import Column

from eventmanager import db
from datetime import datetime
import enum


class Rating(int, enum.Enum):
    one: int = 1
    two: int = 2
    three: int = 3
    four: int = 4
    five: int = 5


class Registration(db.Model):

    __tablename__='registrations'
    # id = db.Column(db.Integer, unique=True)
    registration_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # todo should user_id and event_id be primary key?
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, primary_key=True)
    # user can write review only when registered the event.
    # added an extra column here to record review.
    # review can be null if no reviews added.
    # An extra review db table is not needed, but review collections still exist in API representation.

    # review includes: content, rating and creation time.
    review_time: Column = db.Column(db.DateTime, default=None)
    review_content = db.Column(db.String(100), default=None)
    review_rating = db.Column(db.Enum(Rating), default=None)

    def __repr__(self):
        return f"Registration('{self.event_id}', '{self.user_id}', '{self.registration_time}', " \
            f" review: '{self.review_time}', '{self.review_content}', '{self.review_rating}')"
