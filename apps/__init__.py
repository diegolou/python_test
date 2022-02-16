
from flask import Flask
from importlib import import_module


def register_blueprints (app):
  for module_name in ('authentication', 'home', 'dashboard', 'errors'):
    module = import_module(f'apps.{module_name}.routes')
    app.register_blueprint (module.blueprint)

def create_app():
  app = Flask(__name__)
  app.secret_key = "2esF6NC6Tmmyk/bNYCOda5mOfOq4GMN4VnGEqoKtwTBY6hXT5TcUSQgKtGTx1N/cflBqOVbyyVry7wlS2Yc8hw==,"
  register_blueprints (app)
  return app

