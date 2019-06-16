import os
from flask import Flask, jsonify

from model_manager import ModelManager


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])


@app.before_first_request
def instantiate_model_manager():
    """ This function runs at application startup it loads all of the model found in the configuration """
    model_manager = ModelManager()
    model_manager.load_models(configuration=app.config["MODELS"])


@app.route("/api/models", methods=['GET'])
def get_models():
    """  """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    model_object = model_manager.get_models()

    return jsonify(model_object)


@app.route("/api/models/<qualified_name>/metadata", methods=['GET'])
def get_metadata(qualified_name):
    """  """
    model_manager = ModelManager()
    metadata = model_manager.get_model_metadata(qualified_name=qualified_name)

    if metadata is not None:
        return jsonify(metadata)
    else:
        return jsonify({"type": "ERROR", "message": "Model not found."}), 404


@app.route("/api/models/<qualified_name>/predict", methods=['POST'])
def predict(qualified_name):
    model_manager = ModelManager()
    model_object = model_manager.get_model(qualified_name=qualified_name)

    # making a prediction with the model object
    try:
        prediction = model_object.predict()
        return jsonify(prediction)
    except:
        return "Error", 500


if __name__ == '__main__':
    app.run()
