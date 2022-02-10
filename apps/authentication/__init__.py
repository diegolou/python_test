from flask import Blueprint

blueprint = Blueprint (
  'authen', 
  __name__, 
  url_prefix='',
  template_folder='templates',
  
)