PY = $(shell python3)
PIP = $(shell pip)

deploy:
	${PY} app.py

install:
	${PIP} install -r requirements.txt

test:
	#${PY} -m unittest discover tests
	tox