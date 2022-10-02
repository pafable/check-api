PY = $(shell python3)
PIP = $(shell pip3)
TOX = $(shell tox)

deploy:
	${PY} app.py

install:
	${PIP} install -r requirements.txt

test:
	#${PY} -m unittest discover tests
	${TOX}