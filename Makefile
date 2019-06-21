TEST_PATH=./

.DEFAULT_GOAL := help

.PHONY: help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

clean-pyc: ## Remove python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-build: ## Remove build artifacts.
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info

test: clean-pyc ## Run unit test suite.
	py.test --verbose --color=yes $(TEST_PATH)

start-server: ## start the local development server
	export APP_SETTINGS="model_service.config.DevelopmentConfig"; export FLASK_APP=model_service; export FLASK_DEBUG=1; flask run

test-models-endpoint:
	curl --request GET --url http://localhost:5000/api/models

test-metadata-endpoint:
	curl --request GET --url http://localhost:5000/api/models/iris_model/metadata

test-predict-endpoint:
	curl --request POST --url http://localhost:5000/api/models/iris_model/predict \
	--header 'content-type: application/json' \
	--data '{"petal_length": 1.0, "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}'
