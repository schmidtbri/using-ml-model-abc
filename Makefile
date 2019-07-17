TEST_PATH=./

.DEFAULT_GOAL := help

.PHONY: help venv dependencies test-dependencies clean-pyc test start-server test-models-endpoint test-metadata-endpoint test-predict-endpoint

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

venv: ## create virtual environment
	python3 -m venv venv

dependencies: ## install dependencies from requirements.txt
	pip install -r requirements.txt

test-dependencies: ## install dependencies from test_requirements.txt
	pip install -r test_requirements.txt

clean-pyc: ## Remove python artifacts.
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

clean-test:	## Remove test artifacts
	rm -rf .pytest_cache

test: clean-pyc ## Run unit test suite.
	export APP_SETTINGS="model_service.config.DevelopmentConfig"; \
	export FLASK_APP=model_service; \
	py.test --verbose --color=yes $(TEST_PATH)

start-server: ## start the local development server
	export APP_SETTINGS="model_service.config.DevelopmentConfig"; \
	export FLASK_APP=model_service; \
	export FLASK_DEBUG=1; \
	flask run

test-models-endpoint: ## test the models endpoint
	curl --request GET --url http://localhost:5000/api/models

test-metadata-endpoint: ## test the metadata endpoint
	curl --request GET --url http://localhost:5000/api/models/iris_model/metadata

test-predict-endpoint: ## test the predict endpoint
	curl --request POST --url http://localhost:5000/api/models/iris_model/predict \
	--header 'content-type: application/json' \
	--data '{"petal_length": 1.0, "petal_width": 1.0, "sepal_length": 1.0, "sepal_width": 1.0}'
