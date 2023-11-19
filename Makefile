.PHONY: install run init-db

VENV_DIR := venv

install:
	python3 -m venv $(VENV_DIR)
	. .$(VENV_DIR)/bin/activate; \
	pip install -r requirements.txt

run:
	. .$(VENV_DIR)/bin/activate; \
	python3 run.py

test:
	. .$(VENV_DIR)/bin/activate; \
	pytest