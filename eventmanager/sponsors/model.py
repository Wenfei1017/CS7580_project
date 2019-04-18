from eventmanager import db

# Will not use sponsor
class Sponsor():
    id = db.Column(db.Integer,primary_key=True)
    # events = db.relationship('Event', backref='author', lazy=True)

    # def __repr__(self):
    #     return f"Sponsor('{self.username}', '{self.email}')"
