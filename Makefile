freeze:
	python3 -m pip freeze > requirements.txt

install-reqs:
	python3 -m pip install -r requirements.txt

venv:
	python3 -m venv venv
	@echo 'Source with source venv/bin/activate'

train-model: # Will train a basic mnist model
	python3 train_model.py --save-model --epochs 1

attack-demo-pickle: # Will demonstrate the injection and execution of a pickle file using pickle
	python3 -m pickle-injection --pickle mnist_cnn.pt --pickle-execute

attack-demo-torch: # Will demonstrate the injection and execution of a pickle file using torch
	python3 -m pickle-injection --pickle mnist_cnn.pt --torch-execute