freeze:
	python3 -m pip freeze > requirements.txt

install-reqs:
	python3 -m pip install -r requirements.txt

venv:
	python3 -m venv venv
	@echo 'Source with source venv/bin/activate'

train-model: # Will train a basic mnist model
	python3 train_model.py --save-model --epochs 1

demo: train-model
	python3 -m pickle-injection --pickle mnist_cnn.pt --torch-execute

demo-minecraft: train-model
	python3 -m pickle-injection --pickle mnist_cnn.pt --example minecraft --torch-execute

demo-neofetch: train-model
	python3 -m pickle-injection --pickle mnist_cnn.pt --example neofetch --torch-execute

demo-helloworld: train-model
	python3 -m pickle-injection --pickle mnist_cnn.pt --example location --torch-execute

clean:
	rm *.pt || true
	rm *.altered || true