from pydoc import doc
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

firebase_sdk = credentials.Certificate('phyton-proyect-firebase-adminsdk-91wa9-dfbca6ae49.json')

firebase_admin.initialize_app(firebase_sdk)

db = firestore.client()

doc_ref = db.collection ('building').document('building0000')
doc_ref.set({
    'name': 'vita118',
    'nit': '00000000'

})