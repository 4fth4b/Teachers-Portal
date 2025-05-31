from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(teacher_id):
    return Teacher.query.get(int(teacher_id))


class Teacher(db.Model, UserMixin):
    __tablename__ = 'teachers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    marks = db.Column(db.Integer, nullable=False)

    teacher = db.relationship('Teacher', backref=db.backref('students', lazy=True))