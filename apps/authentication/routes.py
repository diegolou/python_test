# Imports 

import firebase_admin

from flask import Blueprint, request, render_template

from firebase_admin import credentials, auth
from apps.authentication import blueprint
from apps.authentication.forms import CreateAccount, LoginAccount

# Initialize firebase 
cred = credentials.Certificate ('fbAdminConfig.json')
firebase = firebase_admin.initialize_app (cred)

@blueprint.route('/signup', methods=["GET","POST"])
#Register Page
def signup():
  diccionary = {
      'titulo': 'Registro de Nueva Propiedad Horizantal'
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
      print (f"User Already Exists on the DB")
      pass
    except BaseException as err:
      print(f"Unexpected {err=}, {type(err)=}")
      raise
  return render_template('signup.html', data= diccionary, form=form)



#Login Page
@blueprint.route('/signin', methods=["GET","POST"])
def login():
  return render_template('signin.html')

