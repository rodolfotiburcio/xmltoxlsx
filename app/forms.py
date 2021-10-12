from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields.simple import MultipleFileField, SubmitField

class UploadFiles(FlaskForm):
    files = MultipleFileField('Archivos XML', validators=[FileAllowed(['xml'], 'Solo archivos XML')])
    submit = SubmitField('Subir archivos')