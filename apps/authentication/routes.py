# Imports 
import firebase_admin   # Firebase library 
import requests         # To post requests to firebase
import json             # To stringify the request

from flask import redirect, request, render_template, url_for
from firebase_admin import credentials, auth
from dotenv import dotenv_values
from apps import dashboard
from apps import authentication

from apps.authentication import blueprint
from apps.authentication.email_send import send_email_verification
from apps.authentication.forms import CreateAccount, LoginAccount

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
        email=request.form['phemail'].strip(),
        email_verified=False,
        phone_number=request.form['phphone'].strip(),
        password=request.form['phpassword'].strip(),
        display_name=request.form['phname'].strip(),
        disabled=False)
      
      data = {
        'link' : auth.generate_email_verification_link (user.email, auth.ActionCodeSettings(url='http://localhost:4200/signin'))
      }  
      send_email_verification (request.form['phemail'].strip(),link=data['link'])
      return render_template ('verify_new_account.html', data=data)
    except auth.EmailAlreadyExistsError:
      diccionary['error'] = 'La direccón de correo electrónico ya se encuentra registrada. Favor'
      diccionary['loginb'] = True
      
      
    except BaseException as err:
      diccionary['error'] = f"Unexpected {err=}, {type(err)=}"
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
          link= {"link": auth.generate_email_verification_link(details['email'])}
          return render_template('verify_new_account.html', data=link)
        else:
          return redirect(url_for('dashboard.welcome'))
    except BaseException as err:
      diccionary['error'] = f'Unexpected {err} = {type(err)=}'
      diccionary['loginb'] = True

  return render_template('signin.html', data= diccionary, form=form)

