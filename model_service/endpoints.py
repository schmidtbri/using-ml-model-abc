import json
from flask import jsonify, request, Response
from ml_model_abc import MLModelSchemaValidationException

from model_service import app
from model_service.model_manager import ModelManager
from model_service.schemas import ModelCollectionSchema, ModelMetadataSchema, ErrorSchema

model_collection_schema = ModelCollectionSchema()
model_metadata_schema = ModelMetadataSchema()
error_schema = ErrorSchema()


@app.route("/api/models", methods=['GET'])
def get_models():
    """ List of models available
    ---
    get:
      responses:
        200:
          description: List of model available
          content:
            application/json:
              schema: ModelCollectionSchema
    """
    # instantiating ModelManager singleton
    model_manager = ModelManager()

    # retrieving the model object from the model manager
    models = model_manager.get_models()
    response_data = model_collection_schema.dumps(dict(models=models)).data
    return response_data, 200


@app.route("/api/models/<qualified_name>/metadata", methods=['GET'])
def get_metadata(qualified_name):
    """ Metadata about one model
    ---
    get:
      parameters:
        - in: path
          name: qualified_name
          schema:
            type: string
          required: true
          description: The qualified name of the model for which metadata is being requested.
      responses:
        200:
          description: Metadata about one model
          content:
            application/json:
              schema: ModelMetadataSchema
        404:
          description: Model not found.
          content:
            application/json:
              schema: ErrorSchema
    """
    model_manager = ModelManager()
    metadata = model_manager.get_model_metadata(qualified_name=qualified_name)
    if metadata is not None:
        response_data = model_metadata_schema.dumps(metadata).data
        return Response(response_data, status=200, mimetype='application/json')
    else:
        response = dict(type="ERROR", message="Model not found.")
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=400, mimetype='application/json')


@app.route("/api/models/<qualified_name>/predict", methods=['POST'])
def predict(qualified_name):
    """ endpoint that uses a model to make a prediction
    ---
    get:
      parameters:
        - in: path
          name: qualified_name
          schema:
            type: string
          required: true
          description: The qualified name of the model being used for prediction.
      responses:
        200:
          description: Prediction is succesful. The schema of the body of the response is described by the model's output schema.
        400:
          description: Input is not valid JSON or does not meet the model's input schema.
          content:
            application/json:
              schema: ErrorSchema
        404:
          description: Model not found.
          content:
            application/json:
              schema: ErrorSchema
        500:
          description: Server error.
          content:
            application/json:
              schema: ErrorSchema
    """
    # attempting to deserialize JSON in body of request
    try:
        data = json.loads(request.data)
    except json.decoder.JSONDecodeError as e:
        response = dict(type="DESERIALIZATION_ERROR", message=str(e))
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=400, mimetype='application/json')

    # getting the model object from the Model Manager
    model_manager = ModelManager()
    model_object = model_manager.get_model(qualified_name=qualified_name)

    # returning a 404 if model is not found
    if model_object is None:
        response = dict(type="ERROR", message="Model not found.")
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=404, mimetype='application/json')

    try:
        prediction = model_object.predict(data)
        return jsonify(prediction), 200
    except MLModelSchemaValidationException as e:
        # responding with a 400 if the schema does not meet the model's input schema
        response = dict(type="SCHEMA_ERROR", message=str(e))
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=400, mimetype='application/json')
    except Exception as e:
        response = dict(type="ERROR", message="Could not make a prediction.")
        response_data = error_schema.dumps(response).data
        return Response(response_data, status=500, mimetype='application/json')
