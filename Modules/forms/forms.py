from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class addUsbDriveForm(FlaskForm):
    serial_no = StringField('S/N', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class deleteUsbDriveForm(FlaskForm):
    serial_no = StringField('S/N', validators=[DataRequired()])
    submit = SubmitField('Supprimer')