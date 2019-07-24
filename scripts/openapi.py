from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin

from model_service import __doc__
from model_service.schemas import *
from model_service.endpoints import *

spec = APISpec(
    openapi_version="3.0.2",
    title='Model Service',
    version='0.1.0',
    info=dict(description=__doc__),
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

spec.components.schema("ModelSchema", schema=ModelSchema)
spec.components.schema("ModelCollectionSchema", schema=ModelCollectionSchema)
spec.components.schema("JsonSchemaProperty", schema=JsonSchemaProperty)
spec.components.schema("JSONSchema", schema=JSONSchema)
spec.components.schema("ModelMetadataSchema", schema=ModelMetadataSchema)
spec.components.schema("ErrorSchema", schema=ErrorSchema)

with app.test_request_context():
    spec.path(view=get_models)
    spec.path(view=get_metadata)
    spec.path(view=predict)

with open('../openapi_specification.yaml', 'w') as f:
    f.write(spec.to_yaml())
