# Imports 

import firebase_admin

from flask import Blueprint, request, render_template

from firebase_admin import credentials, auth
from apps.dashboard import blueprint




@blueprint.route('/welcome', methods=["GET","POST"])
#Register Page
def welcome():
  diccionary = {
      'titulo': 'Registro de Nueva Propiedad Horizantal',
      'error': '',
      'loginb': False
  }

  return render_template('welcome.html', data= diccionary)




