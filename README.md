# Model Service
Code showing how to use a model based on the ML model base class.

This code is used in this [blog post](https://medium.com/@brianschmidt_78145/using-the-ml-model-base-class-7b984edf47c5).

## Installation 
The makefile included with this project contains targets that help to automate several tasks.

To download the source code execute this command:
```bash
git clone https://github.com/schmidtbri/using-ml-model-abc
```
Then create a virtual environment and activate it:
```bash

# go into the project directory
cd using-ml-model-abc

make venv

source venv/bin/activate
```

Install the dependencies:
```bash
make dependencies
```

Start the development server:
```bash
make start-server
```

Test the development server with some requests:
```bash
make test-models-endpoint

make test-metadata-endpoint

make test-predict-endpoint
```

## Running the unit tests
To run the unit test suite execute these commands:
```bash

# first install the test dependencies
make test-dependencies

# run the test suite
make test
```
