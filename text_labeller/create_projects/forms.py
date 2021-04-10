from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired


class PrepareDataForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired()])
    content = FileField('Upload Data', validators=[FileAllowed(['csv']), FileRequired()])
    class_labels = StringField('Class Labels (separate with comma e.g. negative, positive, neutral)', validators=[DataRequired()])
    submit = SubmitField('Submit')