from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask.views import MethodView
from flask_login import login_user, logout_user, login_required, current_user

from app import db, bcrypt
from app.models import Teacher, Student
from app.forms import RegistrationForm, LoginForm

main = Blueprint('main', __name__)


class HomeView(MethodView):
    def get(self):
        return "Welcome to the homepage!"

# AUTHENTICATION VIEWS

class RegisterView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        form = RegistrationForm()
        return render_template('register.html', form=form)

    def post(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_user = Teacher.query.filter_by(
                email=form.email.data).first()
            if existing_user:
                flash('Email is already registered.', 'danger')
                return render_template('register.html', form=form)

            hashed_pw = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = Teacher(name=form.name.data,
                           email=form.email.data, password=hashed_pw)
            db.session.add(user)
            db.session.commit()
            flash('Account created. Please log in.', 'success')
            return redirect(url_for('main.login'))

        return render_template('register.html', form=form)


class LoginView(MethodView):
    def get(self):
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))
        form = LoginForm()
        return render_template('login.html', form=form)

    def post(self):
        form = LoginForm()
        if form.validate_on_submit():
            user = Teacher.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash('Login successful.', 'success')
                return redirect(url_for('main.dashboard'))
            flash('Invalid credentials.', 'danger')
        return render_template('login.html', form=form)


class DashboardView(MethodView):
    decorators = [login_required]

    def get(self):
        students = current_user.students
        return render_template('dashboard.html', students=students)


class LogoutView(MethodView):
    decorators = [login_required]

    def get(self):
        logout_user()
        flash('You have been logged out.', 'info')
        return redirect(url_for('main.login'))

# STUDENT MANAGEMENT VIEWS  

class StudentAddAPI(MethodView):
    decorators = [login_required]

    def post(self):
        data = request.get_json()
        name = data.get('name')
        subject = data.get('subject')
        marks = data.get('marks')

        if not all([name, subject, marks]):
            return jsonify({'error': 'Missing data'}), 400

        try:
            marks = int(marks)
        except ValueError:
            return jsonify({'error': 'Marks must be an integer'}), 400

        student = Student.query.filter_by(
            name=name, subject=subject, teacher_id=current_user.id).first()

        if student:
            student.marks += marks
        else:
            student = Student(name=name, subject=subject,
                              marks=marks, teacher_id=current_user.id)
            db.session.add(student)

        db.session.commit()

        return jsonify({
            'id': student.id,
            'name': student.name,
            'subject': student.subject,
            'marks': student.marks
        })


class StudentEditAPI(MethodView):
    decorators = [login_required]

    def put(self, student_id):
        student = Student.query.get_or_404(student_id)
        data = request.get_json()
        student.name = data.get('name', student.name)
        student.subject = data.get('subject', student.subject)
        student.marks = data.get('marks', student.marks)

        db.session.commit()
        return jsonify({
            'id': student.id,
            'name': student.name,
            'subject': student.subject,
            'marks': student.marks
        })


class StudentDeleteAPI(MethodView):
    decorators = [login_required]

    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)

        if student.teacher_id != current_user.id:
            return jsonify({'error': 'Unauthorized action'}), 403

        db.session.delete(student)
        db.session.commit()
        return jsonify({'message': f'Student {student.name} deleted successfully'})
