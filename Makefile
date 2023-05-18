APP = api

.PHONY: clean init

init: clean
	cp env-sample .env
	poetry env use python3
	poetry install 

lint:
	poetry run flake8 ${APP}

format:
	poetry run black ${APP}
	poetry run isort ${APP}

test:
	poetry run pytest -vv ${APP}/tests

clean:
	find . -type f -name '*.py[co]' -delete
	find . -type d -name '__pycache__' -delete
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .hypothesis
	rm -rf .pytest_cache
	rm -rf .tox
	rm -f report.xml
	rm -f coverage.xml
