# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, NumberRange, EqualTo
from wtforms.fields.html5 import URLField, DateField, IntegerRangeField, EmailField
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, RadioField, DecimalField
from wtforms_components import TimeField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')
    role = SelectField('Role',choices=[("Teacher","Teacher"),("Student","Student")])
    age = IntegerField()

class ConsentForm(FlaskForm):
    adult_fname = StringField('First Name',validators=[DataRequired()])
    adult_lname = StringField('Last Name',validators=[DataRequired()])
    adult_email = EmailField('Email',validators=[Email()])
    consent = RadioField('Do you want your parents or teachers to see your sleep data/graph', choices=[(True,"True"),(False,"False")])
    submit = SubmitField('Submit')

class SleepForm(FlaskForm):
    rating = SelectField("How would you rate your sleep: 5 is great, 1 is poor", choices=[(None,'---'),(1,1),(2,2),(3,3),(4,4),(5,5)], validators=[DataRequired()])
    starttime = TimeField("Start Time")   
    endtime = TimeField("End Time")   
    feel = SelectField("How did you feel when you woke up: 5 is great, 1 is poor", choices=[(None,'---'),(1,1),(2,2),(3,3),(4,4),(5,5)], validators=[DataRequired()])
    sleep_date = DateField("What date did you go to sleep")
    wake_date = DateField("What date did you wake up")
    minstosleep = IntegerField("How many minutes did it take you to fall asleep?", validators=[NumberRange(min=0,max=180, message="Enter a number between 0 and 180.")])
    submit = SubmitField("Submit")

class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Blog')
    rating = IntegerField()

class AnimalForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    animalname = StringField('Animal Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class TeacherForm(FlaskForm):
    teacher_fname = StringField('First Name', default = 'Jane', validators=[DataRequired()])
    teacher_lname = StringField('Last Name', default = 'Doe', validators=[DataRequired()])
    teacher_email = EmailField('Email', default = 'jane.doe@ousd.org', validators=[Email()])
    teacher_pronouns = StringField('Pronouns', default = 'She/her')
    teacher_room = StringField('Room Number', default = '100', validators=[DataRequired()])
    subject_taught = StringField('Course', default = 'English', validators=[DataRequired()])
    teacher_academy = StringField('Academy', default = 'None')
    submit = SubmitField('Submit')

class TeacherReviewForm(FlaskForm):
    five_star_rating = DecimalField('Five Star Rating', validators=[NumberRange(0, 5, "Make sure you are within the range between 0 and 5")])
    stress_rating = DecimalField('Stress Rating', validators=[NumberRange(0, 5, "Make sure you are within the range between 0 and 5")])
    difficulty_rating = DecimalField('Difficulty Rating', validators=[NumberRange(0, 5, "Make sure you are within the range between 0 and 5")])
    listen_to_music = RadioField('Yes, No or Sometimes: Can you Listen to music during class?', choices=[("Yes"), ("No"), ("Sometimes")], validators=[DataRequired()])
    breaks_during_class = RadioField('Yes, No, or Sometimes: Do you get breaks during class?', choices=[("Yes"), ("No"), ("Sometimes")], validators=[DataRequired()])
    games_in_lesson = RadioField('Yes, No, or Sometimes: Are games incorporated into the lesson plan?', choices=[("Yes"), ("No"), ("Sometimes")], validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class ClinicForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streetAddress = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')