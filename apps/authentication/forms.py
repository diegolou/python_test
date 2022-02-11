
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TelField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp

class CreateAccount (FlaskForm):
  phname = StringField("Nombre de la PH", validators=[DataRequired(message='Campo Obligatorio'), Length(max=64, min=4)],render_kw={"placeholder": "Nombre de la Propiedad Horizontal..."})
  phemail= StringField("Correo Electrónico", validators=[DataRequired(message='Campo Obligatorio'), Email(message='Favor Introducir un correo electrónico valido')],render_kw={"placeholder": "propiedadhorizontal@proveedor.com"})
  phphone= TelField("No de Teléfono", validators=[DataRequired(message='Campo Obligatorio'), Length(max=13, min=12), Regexp (r"\+\d{1,2}\d{10}", message="El No de Teléfono no es valido")  ],render_kw={"placeholder": "+573000000000"})
  phpassword= PasswordField("Nueva Contraseña", validators=[DataRequired(message='Campo Obligatorio'), Length(min=6, message='La contraseña debe tener mínimo 6 caracteres'),EqualTo('phconfirm', message='Constraseñas deben ser iguales')],render_kw={"placeholder": "Contraseña"})
  phconfirm = PasswordField("Repetir Constraseña",render_kw={"placeholder": "Confirmación"})
  phtyc = BooleanField ('términos y Condiciones', validators=[DataRequired()])
  phtdp = BooleanField ('personales', validators=[DataRequired()])
  submit = SubmitField ('Registrar')

class LoginAccount (FlaskForm):
  phemail= StringField("Correo Electrónico", validators=[DataRequired(message='Campo Obligatorio'), Email(message='Favor Introducir un correo electrónico valido')],render_kw={"placeholder": "propiedadhorizontal@proveedor.com"})
  phpassword= PasswordField("Contraseña", validators=[DataRequired(message='Campo Obligatorio')],render_kw={"placeholder": "Contraseña"})  
  submit = SubmitField ('Ingresar')

