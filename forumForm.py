from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, TextField, TextAreaField
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import FileField
from wtforms.validators import DataRequired, EqualTo, Length


class ForumForm(FlaskForm):
    subject = StringField(label='subject: ', validators=[DataRequired()])
    message_text = TextAreaField(label='message_text: ', validators=[DataRequired()])

    photo = FileField('image', validators=[FileRequired()])

        # , FileAllowed(['jpg', 'png', 'JPEG'], 'Images only')])
    submit = SubmitField(label='Submit')