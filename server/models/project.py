from server.config import db
from datetime import date

class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)  # For now, we won’t enforce a real User
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    start_date = db.Column(db.Date, default=date.today)
    end_date = db.Column(db.Date)

    tasks = db.relationship('Task', backref='project', cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'location': self.location,
            'start_date': str(self.start_date),
            'end_date': str(self.end_date) if self.end_date else None
        }
