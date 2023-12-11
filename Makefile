test:
	pytest tests

coverage:
	pytest tests --doctest-modules -v --cov-report term-missing --cov=hackernews
	pytest hackernews --pycodestyle

build:
	echo "0.0.0-dev" > version.txt
	python setup.py develop