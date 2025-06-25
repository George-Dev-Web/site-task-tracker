from app import create_app
from config import db
from models.user import User
from models.project import Project
from models.task import Task
from models.assignee import Assignee

from datetime import date

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create users
    user1 = User(username="engineer1")
    user1.set_password("password123")

    user2 = User(username="foreman")
    user2.set_password("buildit")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Create projects
    project1 = Project(
        name="Nairobi Flyover",
        location="Nairobi",
        start_date=date(2025, 6, 1),
        end_date=date(2025, 12, 15),
        user_id=user1.id
    )
    db.session.add(project1)
    db.session.commit()

    # Create tasks
    task1 = Task(title="Foundation", description="Excavate and pour concrete", status="ongoing", project_id=project1.id)
    task2 = Task(title="Columns", description="Set up steel columns", status="pending", project_id=project1.id)

    db.session.add_all([task1, task2])
    db.session.commit()

    # Create assignees
    assignee1 = Assignee(name="John Doe", role="Site Foreman")
    assignee2 = Assignee(name="Alice W.", role="Crane Operator")

    db.session.add_all([assignee1, assignee2])
    db.session.commit()

    # Assign assignees to tasks
    task1.assignees.append(assignee1)
    task2.assignees.append(assignee2)

    db.session.commit()

    print("✅ Seed data added successfully.")
