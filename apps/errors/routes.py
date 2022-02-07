from apps.errors import blueprint
from flask import render_template


@blueprint.app_errorhandler(404)
def handle_404 (error):
  diccionary = {
      'titulo': 'Page Not Found'
  }
  return render_template ('404.html', data= diccionary), 404


