from flask import jsonify

from model_service import app
from model_service.model_manager import ModelManager


@app.route("/api/models", methods=['GET'])
def get_models():
    """ endpoint that returns a list of models """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    model_object = model_manager.get_models()

    return jsonify(model_object), 200


@app.route("/api/models/<qualified_name>/metadata", methods=['GET'])
def get_metadata(qualified_name):
    """ endpoint that returns metadata about a single model """
    model_manager = ModelManager()
    metadata = model_manager.get_model_metadata(qualified_name=qualified_name)

    if metadata is not None:
        return jsonify(metadata), 200
    else:
        return jsonify({"type": "ERROR", "message": "Model not found."}), 404


@app.route("/api/models/<qualified_name>/predict", methods=['POST'])
def predict(qualified_name):
    """ endpoint that uses a model to make a prediction """
    model_manager = ModelManager()
    model_object = model_manager.get_model(qualified_name=qualified_name)

    # making a prediction with the model object
    try:
        prediction = model_object.predict()
        return jsonify(prediction)
    except:
        return jsonify({"type": "ERROR", "message": "Could not make a prediction."}), 500
