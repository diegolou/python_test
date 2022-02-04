from ast import Pass
from email import message
from xmlrpc.client import Boolean
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class CreateAccount (FlaskForm):
  phname = StringField("Nombre de la PH", validators=[DataRequired(message='Campo Obligatorio'), Length(max=64, min=4)])
  phemail= StringField("Correo Electrónico", validators=[DataRequired(message='Campo Obligatorio'), Email(message='Favor Introducir un correo electrónico valido')])
  phpassword= PasswordField("Nueva Contraseña", validators=[DataRequired(message='Campo Obligatorio'), Length(min=6, message='La contraseña debe tener mínimo 6 caracteres'),EqualTo('phconfirm', message='Constraseñas deben ser iguales')])
  phconfirm = PasswordField("Repetir Constraseña")
  phtyc = BooleanField ('Aceptar términos y Condiciones', validators=[DataRequired()])
  submit = SubmitField ('Registrar')


