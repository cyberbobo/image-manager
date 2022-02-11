from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class addUsbDriveForm(FlaskForm):
    serial_no = StringField('S/N', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class deleteUsbDriveForm(FlaskForm):
    serial_no = StringField('S/N', validators=[DataRequired()])
    submit = SubmitField('Supprimer')

class addTargetForm(FlaskForm):
    name = StringField('target', validators=[DataRequired()])
    tgt_type = StringField('tgt_type', validators=[DataRequired()])
    recommended_save_freq = IntegerField('freq', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class deleteTargetForm(FlaskForm):
    name = StringField('target', validators=[DataRequired()])
    submit = SubmitField('Supprimer')

class addToolForm(FlaskForm):
    tool = StringField('tool', validators=[DataRequired()])
    version = StringField('version', validators=[DataRequired()])
    submit = SubmitField('Ajouter')

class deleteToolForm(FlaskForm):
    tool = StringField('tool', validators=[DataRequired()])
    version = StringField('version', validators=[DataRequired()])
    submit = SubmitField('Supprimer')