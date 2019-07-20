from marshmallow import Schema, fields


class ModelSchema(Schema):
    """ A schema for a short description of a model """
    display_name = fields.String(required=True, allow_none=False, description="The display name of the model.")
    qualified_name = fields.String(required=True, allow_none=False, description="The qualified name of the model.")
    description = fields.String(required=True, allow_none=False, description="The description of the model.")
    major_version = fields.Integer(required=True, allow_none=False, description="The major version of the model package.")
    minor_version = fields.Integer(required=True, allow_none=False, description="The minor version of the model package.")


class ModelCollectionSchema(Schema):
    """ A schema for a collection of models """
    models = fields.Nested(ModelSchema, many=True, required=True, allow_none=False, description="A collection of moodels.")


class JsonSchemaProperty(Schema):
    type = fields.String(required=True, allow_none=False)
    description = fields.String(required=False, allow_none=False)


class JSONSchema(Schema):
    """ Top level of a JSON schema document """
    id = fields.String(required=True, allow_none=False)
    schema = fields.String(required=True, allow_none=False, attribute="$schema", load_from="$schema", dump_to="$schema")
    title = fields.String(required=False, allow_none=False)
    type = fields.String(required=True, allow_none=False)
    properties = fields.Dict(keys=fields.String(), values=JsonSchemaProperty)
    required = fields.List(fields.String(), many=True, required=True, allow_none=False)
    additionalProperties = fields.Boolean(required=True, allow_none=False)


class ModelMetadataSchema(ModelSchema):
    """ A schema for a full description of a model. """
    input_schema = fields.Nested(JSONSchema, required=True, allow_none=False, description="The JSON schema of the input of the model.")
    output_schema = fields.Nested(JSONSchema, required=True, allow_none=False, description="The JSON schema of the output of the model.")


class ErrorSchema(Schema):
    """ A schema for returning errors through the api """
    type = fields.String(required=True, allow_none=False, description="The type of error.")
    message = fields.String(required=True, allow_none=False, description="The error message.")
