from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField
from wtforms.validators import DataRequired, EqualTo, Length


class RegisterForm(FlaskForm):
    id = StringField(label='ID: ', validators=[DataRequired()])
    username = StringField(label='username: ', validators=[DataRequired()])
    password1 = PasswordField(label='password: ', validators=[DataRequired(), Length(5, 16, message='password need to longer than 5 chars')])
    password2 = PasswordField(label='confirm password: ', validators=[DataRequired(),Length(5,16, message='wrong password format'),
                                                                    EqualTo('password1', message='Password Inconsistency')])
    # images = UploadSet('images', IMAGES)
    # file = FileField()

    photo = FileField('image', validators=[FileRequired()])
        # , FileAllowed(['jpg', 'png', 'JPEG'], 'Images only')])
    submit = SubmitField(label='Regiter')