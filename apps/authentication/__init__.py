from flask import Blueprint

blueprint = Blueprint (
  'authentication', 
  __name__, 
  url_prefix='',
  template_folder='templates',
  
)