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
	export APP_SETTINGS="model_service.config.DevelopmentConfig"
	export FLASK_APP=model_service
	flask run