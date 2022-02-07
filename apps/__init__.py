
from flask import Flask
from importlib import import_module


def register_blueprints (app):
  for module_name in ('authentication', 'home', 'errors'):
    module = import_module(f'apps.{module_name}.routes')
    app.register_blueprint (module.blueprint)

def create_app():
  app = Flask(__name__)
  app.secret_key = "123456"
  register_blueprints (app)
  return app

