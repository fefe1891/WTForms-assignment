from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Optional, URL, NumberRange

class AddPetForm(FlaskForm):
    """Form for adding pets."""
    
    name = StringField('Pet Name', validators=[InputRequired()])
    species = StringField('Species', validators=[InputRequired()])
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0,max=30)])
    notes = StringField('Notes')
    available = BooleanField('Available')
    submit = SubmitField('Submit')
    
    
class EditPetForm(FlaskForm):
    """Form for editing pets."""
    photo_url = StringField('Photo URL', validators=[Optional(), URL()])
    notes = StringField('Notes')
    available = BooleanField('Available')
    submit = SubmitField('Submit')