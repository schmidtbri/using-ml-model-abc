import importlib

from ml_model_abc import MLModel


class ModelManager(object):
    """ Singleton class that instantiates and manages model objects """
    _models = []

    @classmethod
    def load_models(cls, configuration):
        for c in configuration:
            model_module = importlib.import_module(c["module_name"])
            model_class = getattr(model_module, c["class_name"])
            model_object = model_class()

            if isinstance(model_object, MLModel) is False:
                raise ValueError("The ModelManager can only hold references to objects of type MLModel.")

            # saving the model reference to the models list
            cls._models.append(model_object)

    @classmethod
    def get_models(cls):
        """Get a list of models in the model manager instance."""
        model_objects = [{
            "display_name": model.display_name,
            "qualified_name": model.qualified_name,
            "description": model.description,
            "major_version": model.major_version,
            "minor_version": model.minor_version} for model in cls._models]

        return model_objects

    @classmethod
    def get_model_metadata(cls, qualified_name):
        """Get a model metadata by qualified name."""
        # searching the list of model objects to find the one with the right qualified name
        model_objects = [model for model in cls._models if model.qualified_name == qualified_name]

        if len(model_objects) == 0:
            return None
        else:
            model_object = model_objects[0]
            return {
                "display_name": model_object.display_name,
                "qualified_name": model_object.qualified_name,
                "description": model_object.description,
                "major_version": model_object.major_version,
                "minor_version": model_object.minor_version,
                "input_schema": model_object.input_schema.json_schema("https://example.com/input_schema.json"),
                "output_schema": model_object.output_schema.json_schema("https://example.com/output_schema.json")}

    @classmethod
    def get_model(cls, qualified_name):
        """Get a model object by qualified name."""
        # searching the list of model objects to find the one with the right qualified name
        model_objects = [model for model in cls._models if model.qualified_name == qualified_name]

        if len(model_objects) == 0:
            return None
        else:
            return model_objects[0]
