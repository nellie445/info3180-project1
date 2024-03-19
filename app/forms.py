from flask_wtf import FlaskForm
from  wtforms import StringField, IntegerField, SelectField, TextAreaField, FileField, PasswordField
from  wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileField, FileRequired, FileAllowed 
import os

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators =[DataRequired()])
    description =  TextAreaField("Description", validators=[DataRequired()])
    bedrooms = StringField('Number of Bedrooms',  validators=[DataRequired()])
    bathrooms = StringField('Number of Bathrooms', validators= [DataRequired()])
    
    property_type = SelectField('Type of Property',  choices=[('house','House'), ('townhouse','Townhouse'), ('apartment', 'Apartment')], validate_choice=[DataRequired()])
    price  = StringField('Price', validators= [DataRequired()])
    location = StringField('Location', validators= [DataRequired()])
    
    photo = FileField('Property Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])

    
"""class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email',  validators=[DataRequired(), Email()])
    subject = StringField('Subject',  validators=[DataRequired()])
    message = TextAreaField("Message", validators= [DataRequired()])
    """""
    
class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[FileRequired(), FileAllowed(['jpg', 'png','jpeg'], 'Images only!')])


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    