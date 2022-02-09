# Imports 
import firebase_admin   # Firebase library 
import requests         # To post requests to firebase
import json             # To stringify the request

from flask import request, render_template, url_for
from firebase_admin import credentials, auth
from dotenv import dotenv_values

from apps.authen import blueprint
from apps.authen.forms import CreateAccount, LoginAccount

# Initialize firebase 
cred = credentials.Certificate ('fbAdminConfig.json')
firebase = firebase_admin.initialize_app (cred)
config = dotenv_values(".env")


@blueprint.route('/signup', methods=["GET","POST"])
#Register Page
def signup():
  diccionary = {
      'titulo': 'Registro de Nueva Propiedad Horizantal',
      'error': '',
      'loginb': False
  }

  form = CreateAccount(request.form)

  if form.validate_on_submit():
    try:      
      user = auth.create_user(
        email=request.form['phemail'],
        email_verified=False,
        password=request.form['phpassword'],
        display_name=request.form['phname'],
        disabled=False)
      
      data = {
        'link' : auth.generate_email_verification_link (user.email, auth.ActionCodeSettings(url='http://localhost:4200/signin'))
      }  
      
      return render_template ('verify_new_account.html', data=data)
    except auth.EmailAlreadyExistsError:
      diccionary['error'] = 'La direccón de correo electrónico ya se encuentra registrada. Favor'
      diccionary['loginb'] = True
      
      
    except BaseException as err:
      diccionary['error'] = 'f"Unexpected {err=}, {type(err)=}'
      return render_template('signup.html', data= diccionary, form=form)
      
  return render_template('signup.html', data= diccionary, form=form)



#Login Page
@blueprint.route('/signin', methods=["GET","POST"])
def login():
  diccionary = {
      'titulo': 'Ingresor a Propiedad Horizantal',
      'error': '',
      'loginb': False
  }
  form = LoginAccount(request.form)
  if form.validate_on_submit():
    try:   
      details = {"email": request.form['phemail'],"password": request.form['phpassword'],"returnSecureToken":True}
      vtoken = json.loads(requests.post (f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={config['firebaseConfigapiKey']}",details).content)
    
      
      if 'error' in vtoken.keys():
        
        if vtoken['error'].message == 'EMAIL_NOT_FOUND':
          diccionary['error'] = 'La direccón de correo electrónico no se encuentra registrada. Favor'
          diccionary['loginb'] = True
        elif 'message' == 'INVALID_PASSWORD':
          diccionary['error'] = 'La contraseña es incorrecta favor ingresarla de nuevo'
        elif 'message' == 'USER_DISABLED':
          diccionary['error'] = 'Usuario Inhabilitado. Favor ponerse en contacto con su administrador'
        else:
          diccionary['error'] = f'Error desconocido {vtoken["error"].message} Favor ponerse en contacto con su administrador'
      else:
        return render_template(url_for('welcome.html'))
    except BaseException as err:
      diccionary['error'] = f'Unexpected {err} = {type(err)=}'
      diccionary['loginb'] = True

  return render_template('signin.html', data= diccionary, form=form)

