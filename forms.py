from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileSize, FileAllowed
from wtforms import PasswordField
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, length, equal_to



class Post(FlaskForm):
    title = StringField("Title", validators=[DataRequired(message="title of the post")])
    content = TextAreaField("Main content of the article", validators=[DataRequired()])
    author = StringField("Author's name")
    img = FileField("image",
                    validators=[
                        FileSize(max_size=1024 * 1024 * 20),
                        FileAllowed(["jpg", "png", "jpeg"], message="format not allowed")
                    ])

    submit = SubmitField("Publish")

class RegisterForm(FlaskForm):
    username = StringField("enter your Username", validators=[DataRequired()])
    password = PasswordField("enter your password", validators=[
        length(min=6, max=25),
        DataRequired()
    ])
    repeat_password = PasswordField("repeat your password", validators=[equal_to("password", message="please repeat your password")])

    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    username = StringField("enter your Username", validators=[DataRequired()])
    password = PasswordField("enter your password", validators=[
        length(min=6, max=25),
        DataRequired()
    ])

    submit = SubmitField("Login")