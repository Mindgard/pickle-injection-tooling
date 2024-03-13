freeze:
	python3 -m pip freeze > requirements.txt

install-reqs:
	python3 -m pip install -r requirements.txt

venv:
	python3 -m venv venv
	@echo 'Source with source venv/bin/activate'

train-model: # Will train a basic mnist model
	python3 main.py --save-model --epochs 1

attack-demo:
	python3 attacks/pickle_injection.py --file mnist_cnn.pt --execute