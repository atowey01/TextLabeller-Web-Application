from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, RadioField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, InputRequired


class SelectProjectForm(FlaskForm):
    project = SelectField('Select Project to Label', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Submit')


class LabelDataForm(FlaskForm):
    class_label= RadioField('Select Label', coerce=int, validators=[InputRequired()])
    submit = SubmitField('Submit')