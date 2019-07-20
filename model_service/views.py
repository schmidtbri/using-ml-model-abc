""" Views that display a UI for the model services """
from flask import render_template

from model_service import app
from model_service.model_manager import ModelManager


@app.route('/', methods=['GET'])
def index():
    """ view that displays a list of models """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    models = model_manager.get_models()

    return render_template('index.html', models=models)


@app.route("/models/<qualified_name>/metadata", methods=['GET'])
def display_metadata(qualified_name):
    """ view that displays metadata about a model """
    model_manager = ModelManager()
    model_metadata = model_manager.get_model_metadata(qualified_name=qualified_name)

    if model_metadata is not None:
        return render_template('metadata.html', model_metadata=model_metadata)
    else:
        return render_template('model_not_found.html')


@app.route("/models/<qualified_name>/predict", methods=['GET'])
def display_form(qualified_name):
    """ view that displays the prediction form of a model """
    model_manager = ModelManager()
    model_metadata = model_manager.get_model_metadata(qualified_name=qualified_name)

    return render_template('predict.html', model_metadata=model_metadata)
