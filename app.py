from flask import Flask, render_template, flash, redirect, url_for, request
from forms import StudentForm, TeacherForm
from peewee import *
from datetime import datetime


# create flask app

app = Flask(__name__)
app.secret_key = "code secret"

# create database

db = SqliteDatabase("myschool.db")

class Group(db.Model):
    name = CharField(unique=True)
    created_at = DateTimeField(default=datetime.now, formats='%Y-%m-%d %H:%M:%S')

    class Meta:
        database = db



class Student(db.Model):
    fullname = CharField()
    tel = CharField()
    email = CharField(unique=True)
    joining_date = DateTimeField(default=datetime.now, formats='%Y-%m-%d')
    group = ForeignKeyField(Group, backref='students', null=True)
    
    class Meta:
        database = db
        

class Teacher(db.Model):
    fullname = CharField()
    tel = CharField()
    email = CharField(unique=True)
    experience = IntegerField()
    subject = CharField()
    joining_date = DateTimeField(default=datetime.now, formats='%Y-%m-%d')
    
    class Meta:
        database = db



def initialize_database():
    db.connect()
    db.create_tables([Student, Teacher, Group], safe=True)
    db.close()
    db.close()


with app.app_context():
    initialize_database()


# creating the first route for index page
@app.route("/", methods=['GET', 'POST'])
def home():
    student_count = Student.select().count()
    teacher_count = Teacher.select().count()
    return render_template('index.html',student_count=student_count, teacher_count=teacher_count)


# creating the student route
@app.route("/student", methods=['GET', 'POST'])
def student_list():
    students = Student.select()
    counter = students.count()
    return render_template('student.html',students=students, counter = counter)

# add new student route

@app.route('/student/new', methods=['GET', 'POST'])
def add_student():
    # create a variable with StudentForm() value
    form = StudentForm()
    if request.method == 'POST' and form.validate_on_submit():
        # when the submit button is pressed
        fullname = form.fullname.data
        tel = form.tel.data
        email = form.email.data
        student = Student.create(
            fullname = fullname,
            tel = tel,
            email = email,
        )
        flash('Student added successfully', 'success')
        return redirect(url_for('student_list'))    
    return render_template('student_new.html',form=form)


@app.route('/showdeleteconfirm/<student_id>')
def show_confirmation(student_id):
    student = Student.get_by_id(student_id)
    return render_template('delete_confirm.html', student=student)

@app.route('/deleteteacherconfirmation/<prof_id>')
def teacher_delete_confirm(prof_id):
    teacher = Teacher.get_by_id(prof_id)
    return render_template('teacher_delete_confirm.html', teacher=teacher)



@app.route('/teacher/delete/<int:prof_id>', methods=['POST'])
def delete_teacher(prof_id):
    teacher = Teacher.get_or_none(Teacher.id == prof_id)
    if teacher:
        teacher.delete_instance()
        flash('Teacher deleted successfully!', 'success')
    else:
        flash('Teacher not found.', 'danger')
    return redirect(url_for('teachers_list'))







# Decorator 
@app.route('/teacher')
def teachers_list():   
    # selecting teachers
    query = Teacher.select()
    counter = query.count()
    return render_template('teacher.html', teachers = query, counter = counter)


@app.route('/teacher/new', methods=['POST','GET'])
def add_teacher():
    form = TeacherForm()
    if request.method == 'POST' and form.validate_on_submit():
        
        Teacher.create(
            fullname = form.fullname.data,
            tel = form.tel.data,
            email = form.email.data,
            experience = form.experience.data,
            subject = form.subject.data,
        )
        flash('Teacher has been added successfully!', 'success')
        return redirect(url_for('teachers_list'))
    
    return render_template('teacher_new.html', form = form)



@app.route('/teacher/<int:teacher_id>')
def teacher_info(teacher_id):
    teacher = Teacher.get_by_id(teacher_id)
    return render_template('teacher_view.html', teacher = teacher)

    

@app.route('/schedual')
def schedual():
    return render_template('scheduals.html')













if __name__ == '__main__':
    app.run(debug=True)