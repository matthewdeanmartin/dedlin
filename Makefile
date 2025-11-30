# if you wrap everything in uv run, it runs slower.
ifeq ($(origin VIRTUAL_ENV),undefined)
    VENV := uv run
else
    VENV :=
endif

uv.lock: pyproject.toml
	@echo "Installing dependencies"
	@uv sync

# tests can't be expected to pass if dependencies aren't installed.
# tests are often slow and linting is fast, so run tests on linted code.
test: pylint bandit uv.lock
	@echo "Running unit tests"
	# $(VENV) python -m unittest discover
	$(VENV) py.test tests --cov=dedlin --cov-report=html --cov-fail-under 50


isort:  
	@echo "Formatting imports"
	$(VENV) isort .

black:  isort 
	@echo "Formatting code"
	$(VENV) metametameta pep621
	$(VENV) black dedlin --exclude .venv
	$(VENV) black tests --exclude .venv
	$(VENV) black scripts --exclude .venv

pre-commit:  isort black
	@echo "Pre-commit checks"
	$(VENV) pre-commit run --all-files

bandit:  
	@echo "Security checks"
	$(VENV)  bandit dedlin -r

.PHONY: pylint
pylint:  isort black 
	@echo "Linting with pylint"
	$(VENV) pylint dedlin --fail-under 9.7

check: test pylint bandit pre-commit

.PHONY: publish
publish: test
	rm -rf dist && $(VENV) hatch build

.PHONY:
docker:
	docker build -t dedlin -f Dockerfile .

check_docs:
	$(VENV) interrogate dedlin --verbose
	$(VENV) pydoctest --config .pydoctest.json | grep -v "__init__" | grep -v "__main__" | grep -v "Unable to parse"

make_docs:
	pdoc dedlin --html -o docs --force

check_md:
	$(VENV) mdformat README.md docs/*.md
	# $(VENV) linkcheckMarkdown README.md # it is attempting to validate ssl certs
	$(VENV) markdownlint README.md --config .markdownlintrc

check_spelling:
	$(VENV) pylint dedlin --enable C0402 --rcfile=.pylintrc_spell
	$(VENV) codespell README.md --ignore-words=private_dictionary.txt
	$(VENV) codespell dedlin --ignore-words=private_dictionary.txt

check_changelog:
	# pipx install keepachangelog-manager
	$(VENV) changelogmanager validate

check_all: check_docs check_md check_spelling check_changelog
