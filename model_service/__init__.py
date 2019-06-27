import os
from flask import Flask
from flask_bootstrap import Bootstrap

from model_service.model_manager import ModelManager

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
bootstrap = Bootstrap(app)


import model_service.endpoints
import model_service.views


@app.before_first_request
def instantiate_model_manager():
    """ This function runs at application startup it loads all of the model found in the configuration """
    model_manager = ModelManager()
    model_manager.load_models(configuration=app.config["MODELS"])
