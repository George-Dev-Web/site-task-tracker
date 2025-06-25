from config import db

task_assignees = db.Table(
    'task_assignees',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('assignee_id', db.Integer, db.ForeignKey('assignees.id'), primary_key=True),
    db.Column('hours_spent', db.Float)
)

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending")
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))

    assignees = db.relationship("Assignee", secondary=task_assignees, back_populates="tasks")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "project_id": self.project_id,
            "assignees": [a.to_dict() for a in self.assignees]
        }
