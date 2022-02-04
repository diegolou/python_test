# Required Imports
import re
import firebase_admin
import pyrebase
import json
from firebase_admin import credentials, auth, firestore, initialize_app
from firebase_admin.auth import UserRecord
from flask import Flask, request, jsonify, render_template, redirect, session, url_for
from functools import wraps


# Initialize Flask app
app = Flask (__name__)

#Connect to firebase

cred = credentials.Certificate('fbAdminConfig.json')
firebase = firebase_admin.initialize_app (cred)
pb = pyrebase.initialize_app(json.load(open('fbconfig.json')))

db = firestore.client()
auth = pb.auth()
storage = pb.storage()


#Initialze person as dictionary



# Wrap
def check_token (f):
  @wraps(f)
  def wrap(*args, **kwargs):
    if not request.headers.get ('authorization'):
      return {'message': 'No token provided'}, 400
    try:
      user = auth.verify_id_token(request.headers['authorization'])
      request.user = user
    except:
      return {'message': 'Invalid Token provided.' }, 400
    return f(*args, **kwargs)
  return wrap

#Login
@app.route("/")
def login():
  return render_template("login.html")

#Sign up/ Register
@app.route("/signup")
def signup():
  return render_template("signup.html")

#Welcome page
@app.route("/welcome")
def welcome():
  #if person.uid == True:
    return render_template("welcome.html")
  #else:
  # return redirect(url_for('login'))

#If someone clicks on login, they are redirected to /result
# @app.route("/result", methods = ["POST", "GET"])
# def result():
#   if request.method == "POST":        #Only if data has been posted
#       result = request.form           #Get the data
#       email = result["email"]
#       password = result["pass"]
#       try:
#           #Try signing in the user with the given information
#           user = auth.sign_in_with_email_and_password(email, password)
#           #Insert the user data in the global person
#           global person
#           ["is_logged_in"] = True
#           person["email"] = user["email"]
#           person["name"] = user["displayName"]
#           person["uid"] = user["localId"]
#           #Get the name of the userperson
#           data = pb.child("users").get()
#           person["name"] = data.val()[person["uid"]]["name"]
#           #Redirect to welcome page
#           return redirect(url_for('welcome'))
#       except:
#           #If there is any error, redirect back to login
#           return redirect(url_for('login'))
#   else:
#     if person["is_logged_in"] == True:
#       return redirect(url_for('welcome'))
#     else:
#       return redirect(url_for('login'))

# Register a new building redirect to /register
@app.route("/register", methods = ["POST", "GET"])
def register():
  if request.method == "POST":        #Only listen to POST
    result = request.form           #Get the data submitted
    pag_email = result["email"]
    pag_password = result["pass"]
    pag_display_name = result["name"]

    if pag_email is None or pag_password is None or pag_display_name is None:
      return {'message': 'Opps!!! Error missing emial or passaword or name .....'}

    try:
      #Try creating the user account using the provided data
      user = auth.create_user(email=pag_email, password=pag_password, display_name=pag_display_name, email_verified=False)
      
      
      return redirect(url_for('welcome'))
    except:
      return {'message': 'Opps Error creating user'}, 400

  else:
    #if person.uid == True:
    #    return redirect(url_for('welcome'))
    #else:
        return redirect(url_for('register'))


# Initialize Firebase Db.
#cred = credentials.Certificate('phyton-proyect-firebase-adminsdk-91wa9-dfbca6ae49.json')
#default_app = initialize_app (cred)
#db = firestore.client()
#building_ref = db.collection('building')

# Things to do before the request
@app.before_request
def before_request():
  print ("Antes de Petición")

# Things to do after request
@app.after_request
def after_request(response):
  print ("Después de la petición")
  return response

# Create Home Path
@app.route ('/')
def index ():
  # Create Dictionary to frameWork.
  data = {
    'titulo': 'Software de Administración de Propiedad Horizontal',
    'bienvenida': 'Saludos!'
  }
  
  # Render Page and Passing Dictionary. 
  return render_template('login.html', data=data)

# Create Aboute Path.
@app.route('/login')
def about():
  return render_template('login.html')

# Create Building Page with parameters
@app.route('/building/<name>')
def building (name):
  data = {
    'titulo': 'Bienvenido Edificio',
    'name' : name
  }
  return render_template('building.html', data=data)

# Create a request with multiple parameters
def query_building():
  print (request)
  print (request.args)
  print (request.args.get('BId'))
  return "OK"

# Check the DB.
@app.route ('/building', methods=['GET'])
def list_of_buildings ():
  data={}
  try:
    BId = request.args.get('BId')
    # Check if BId parameter was passed to URL Query
    if (BId):
#      bId= building_ref.document(BId).get()
      data['message']= 'Exito'
#      return jsonify(bId.to_dict()), 200
    else:
#      all_bIds = [doc.to_dict() for doc in building_ref.stream()]
      data['message']= 'Exito'
#      return jsonify(all_bIds)
    
  except Exception as e:
    data['message']='Error'

# Create Page 404 not founf
def page_not_found (error):
  data = {
    'titulo': 'Page Not Found',
    'bienvenida': 'Saludos!'
  }
  return render_template('404.html',data= data), 404
# Run the App
if __name__ == '__main__':
  # Create New Query.
  # app.add_url_rule ('/query_building', view_func=query_building)
  # register the error handler
  app.register_error_handler(404, page_not_found)
  app.run(debug=True, port=4200)


