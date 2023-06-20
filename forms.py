from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, BooleanField
from wtforms.validators import URL, Optional, NumberRange

# accepted_species = ['cat', 'dog', 'porcupine', 'Cat', 'Dog', 'Porcupine']


class AddPetForm(FlaskForm):
    '''form for adding new pet'''

    name = StringField("Pet Name")
    species = SelectField("Species", choices=[
                          ('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')])
    photo_URL = StringField("Photo URL", validators=[
                            URL(message="Must be a valid URL"), Optional()])
    age = IntegerField("Age", validators=[NumberRange(
        min=0, max=30, message="Age has to be between 0 to 30")])
    notes = StringField("Notes")


class EditPetForm(FlaskForm):
    '''form for editting a certain pet'''

    photo_URL = StringField("Photo URL", validators=[
                            URL(message="Must be a valid URL"), Optional()])
    notes = StringField("Notes")
    available = BooleanField('Is pet available?', default=True)
