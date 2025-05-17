from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, DateField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email


class StudentForm(FlaskForm):
    fullname = StringField('Fullname',validators=[DataRequired()])
    tel = StringField('Tel Number',validators=[DataRequired()])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    btn_submit = SubmitField('Add Student')

class TeacherForm(FlaskForm):
    fullname = StringField('Fullname',validators=[DataRequired()])
    tel = StringField('Tel Number',validators=[DataRequired()])
    email = EmailField('Email',validators=[DataRequired(),Email()])
    experience = IntegerField('Teacher Experience Years',validators=[DataRequired()])
    subject = StringField('Subject',validators=[DataRequired()])
    btn_submit = SubmitField('Add Teacher')