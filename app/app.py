
import firebase_admin


from flask import Flask, render_template, request, url_for
from firebase_admin import credentials, auth, firestore
from form import CreateAccount
from email_send import sendemail


# Initialize Flask app

app = Flask (__name__)
app.secret_key = "123456"

# Connect to firebase

cred = credentials.Certificate ('fbAdminConfig.json')
firebase = firebase_admin.initialize_app (cred)


#Home  - Layout - Template
@app.route("/")
def home():
  diccionary   = {
      'titulo': 'Software de Administración de Propiedad Horizontal'
  }
  return render_template ('home.html', data= diccionary)

#Register Page
@app.route('/signup', methods=["GET","POST"])
def signup():
  diccionary = {
      'titulo': 'Registro de Nueva Propiedad Horizantal'
  }
  form = CreateAccount()
  if form.validate_on_submit():
    try:      
      user = auth.create_user(
        email=request.form['phemail'],
        email_verified=False,
        password=request.form['phpassword'],
        display_name=request.form['phname'],
        disabled=False)
      data = {
        'link' : auth.generate_email_verification_link (user.email, auth.ActionCodeSettings(url='http://localhost:4200/login'))
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
@app.route('/login')
def login():
  return render_template('login.html')

#Create Page 404 not found
def error_page (error):
  diccionary = {
      'titulo': 'Page Not Found'
  }
  return render_template ('404.html', data= diccionary), 404

if __name__ == '__main__':
  app.register_error_handler(404, error_page)
  app.run (debug=True, port=4200)