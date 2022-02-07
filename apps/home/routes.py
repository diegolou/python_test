from apps.home import blueprint
from flask import render_template


@blueprint.route('/')
def home():
  diccionary   = {
    'titulo': 'Software de Administración de Propiedad Horizontal'
  }
  return render_template ('home.html', data= diccionary)




