from apps.entities.direccion import DIRECCION
from firebase_admin import firestore


class USUARIO:
  uid = ''
  display_name = ''
  first_name = ''
  last_name = ''
  email = ''
  role = ''
  phone = ''
  direccion = ''
  idToken = ''
  refreshToken = ''
  expiresIn = ''
  

  def __init__(self, uid='', display_name='', email='', role='', phone='', first_name='', last_name='', direccion ='', idToken= '', refreshToken = '', expiresIn = '') -> None:
    self.display_name = display_name
    self.uid = uid
    self.email = email
    self.role = role
    self.phone = phone
    self.first_name = first_name
    self.last_name = last_name
    self.direccion = direccion
    self.idToken = idToken
    self.refreshToken = refreshToken
    self.expiresIn = expiresIn
    

  def create_new_user (self):
    db = firestore.client()
    doc_ref = db.collection(u'users').document(f'{self.uid}')
    doc_ref.set({
      'uid' : self.uid,
      'first_name': self.first_name,
      'last_name': self.last_name,
      'display_name' : self.display_name,
      'email': self.email,
      'role': self.role,
      'phone': self.phone,
      'direccion': self.direccion
    })

