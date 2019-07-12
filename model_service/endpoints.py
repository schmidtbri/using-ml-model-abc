import json
from flask import jsonify, request
from schema import SchemaError

from model_service import app
from model_service.model_manager import ModelManager


@app.route("/api/models", methods=['GET'])
def get_models():
    """ endpoint that returns a list of models """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    models = model_manager.get_models()

    return jsonify(models), 200


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
        data = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        return jsonify({"type": "SCHEMA_ERROR", "message": str(e)}), 400

    try:
        prediction = model_object.predict(data)
        return jsonify(prediction), 200
    except SchemaError as e:
        return jsonify({"type": "SCHEMA_ERROR", "message": "Bad input data: {}".format(str(e))}), 400
    except Exception as e:
        return jsonify({"type": "ERROR", "message": "Could not make a prediction."}), 500
