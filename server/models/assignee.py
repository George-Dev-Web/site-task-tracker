from config import db
from models.task import task_assignees

class Assignee(db.Model):
    __tablename__ = 'assignees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100))

    tasks = db.relationship("Task", secondary=task_assignees, back_populates="assignees")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role
        }
