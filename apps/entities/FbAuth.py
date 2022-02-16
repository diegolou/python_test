
import firebase_admin
import json
import requests 


from firebase_admin import credentials
from flask import url_for
from apps.entities.users import USUARIO
from json import load
from dotenv import dotenv_values


class AUTH:

  cred = ''
  firebase = ''
  rest_apikey = ''
  rest_apiurl = 'https://identitytoolkit.googleapis.com/v1/accounts:'


  def __init__(self) -> None:
    self.cred = credentials.Certificate ('fbAdminConfig.json')
    self.firebase = firebase_admin.initialize_app (self.cred)
    config = dotenv_values(".env")
    self.rest_apikey = config['firebaseConfigapiKey']
    
    
  def createNewBuilding (self, email, password, displayName, phone):
    try:
      
      payload = json.dumps ({"email": email,"password": password, "returnSecureToken":True})
      user = requests.post (f"{self.rest_apiurl}signUp", params = {"key": self.rest_apikey}, data = payload).json() 
      
      if 'error' in user.keys():
        
        raise Exception (user['error'])
      
      usuario = USUARIO( 
        uid =  user['localId'], 
        display_name= displayName, 
        email= user['email'], 
        phone = phone, 
        role='ph_admin',
        idToken= user['idToken'],
        refreshToken=user['refreshToken'],
        expiresIn=user['expiresIn'],
        )
      usuario.create_new_user()
    
      return usuario
    except BaseException as err:
      
      return {
        "code": err.args[0]['code'],
        "message" : err.args[0]['message']
      }
      
  def sendEmailVerificationLink (self, usuario: USUARIO ):
    try:
      details = {"requestType": 'VERIFY_EMAIL',"idToken": usuario.idToken}
      return json.loads(requests.post (f"{self.rest_apiurl}sendOobCode?key={self.rest_apikey}",details).content)
      
    except:
      error = {}
      return

  

