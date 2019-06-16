import unittest
from traceback import print_tb
from iris_application.model_manager import ModelManager


class ModelManagerTests(unittest.TestCase):
    def test1(self):
        # arrange
        # instantiating the model manager class
        model_manager = ModelManager()
        # loading the MLModel objects from configuration
        model_manager.load_models(configuration=[{
            "module_name": "iris_model.iris_predict",
            "class_name": "IrisModel"
        }])

        # act
        exception_raised = False
        model_object = None
        # accessing the IrisModel model object
        try:
            model_object = model_manager.get_model(qualified_name="iris_model")
        except Exception as e:
            exception_raised = True
            print_tb(e)

        # assert
        self.assertFalse(exception_raised)
        self.assertTrue(model_object is not None)



if __name__ == '__main__':
    unittest.main()
