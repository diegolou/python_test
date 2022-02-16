# Imports 

import requests         # To post requests to firebase
import json
import apps.entities.FbAuth as fbAuth

from flask import flash, redirect, request, render_template, url_for
from firebase_admin import auth
from dotenv import dotenv_values
from apps import dashboard
from apps import authentication

from apps.authentication import blueprint
from apps.entities.email_send import send_email_verification
from apps.authentication.forms import CreateAccount, LoginAccount

from apps.entities.users import USUARIO

# Initialize firebase 
firebase = fbAuth.AUTH()
user = None

config = dotenv_values(".env")

# Initialize User

@blueprint.route('/signup', methods=["GET","POST"])
#Register Page
def signup():
  diccionary = {
      'titulo': 'Registro de Nueva Propiedad Horizantal'
  }

  form = CreateAccount(request.form)

  if form.validate_on_submit():  
    user = firebase.createNewBuilding(email= request.form['phemail'].strip(), password=request.form['phpassword'], displayName=request.form['phname'], phone=request.form['phphone'])
    firebase.sendEmailVerificationLink(usuario = user)
    #error = send_email_verification (request.form['phemail'].strip(),link=link)
    flash('Se creo la cuenta con exito')
    return render_template ('verify_new_account.html', data=diccionary)  
    
  return render_template('signup.html', data= diccionary, form=form)



#Login Page
@blueprint.route('/signin', methods=["GET","POST"])
def login():
  diccionary = {
      'titulo': 'Ingresa a Propiedad Horizantal',
      'error': '',
      'loginb': False
  }
  form = LoginAccount(request.form)
  if form.validate_on_submit():
    try:   
      details = {"email": request.form['phemail'].strip(),"password": request.form['phpassword'].strip(),"returnSecureToken":True}
      vtoken = json.loads(requests.post (f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={config['firebaseConfigapiKey']}",details).content)
      if 'error' in vtoken.keys():  
        if vtoken['error']['message'] == 'EMAIL_NOT_FOUND':
          diccionary['error'] = 'La direccón de correo electrónico no se encuentra registrada. Favor Ingresar al modulo de '
          diccionary['loginb'] = True
        elif vtoken['error']['message'] == 'INVALID_PASSWORD':
          diccionary['error'] = 'La contraseña es incorrecta favor ingresarla de nuevo'
        elif vtoken['error']['message'] == 'USER_DISABLED':
          diccionary['error'] = 'Usuario Inhabilitado. Favor ponerse en contacto con su administrador'
        else:
          diccionary['error'] = f'Error desconocido {vtoken["error"]["message"]} Favor ponerse en contacto con su administrador'
      else:
        data = {"idToken": vtoken["idToken"]}
        user_info = json.loads(requests.post (f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={config['firebaseConfigapiKey']}",data).content)
        if 'error' in user_info.keys():
          diccionary['error'] = f'Error desconocido {vtoken["error"]["message"]} Favor ponerse en contacto con su administrador'
        elif user_info['users'][0]['emailVerified'] == False:
          return render_template('verify_new_account.html')
        else:
          return redirect(url_for('dashboard.welcome'))
    except BaseException as err:
      diccionary['error'] = f'Unexpected {err} = {type(err)=}'
      diccionary['loginb'] = True

  return render_template('signin.html', data= diccionary, form=form)

@blueprint.route('verify_new_account.html')
def verify_new_account():
  diccionary = {
    'titulo': 'Bienvenido a Propiedad Horizontal',
    'error': '',
    'loginb': False
  }

  return

