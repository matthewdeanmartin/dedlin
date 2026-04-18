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

.PHONY: docker
docker:
	docker build -t dedlin -f Dockerfile_local .

.PHONY: docker-run
docker-run:
	bash ./scripts/docker_run.sh --version

check_docs:
	$(VENV) interrogate dedlin --verbose
	$(VENV) pydoctest --config .pydoctest.json | grep -v "__init__" | grep -v "__main__" | grep -v "Unable to parse"

make_docs:
	pdoc dedlin --html -o docs --force

check_md:
	$(VENV) mdformat README.md docs/*.md
	$(VENV) markdownlint README.md --config .markdownlintrc

.PHONY: linkcheck
linkcheck:
	@echo "Checking links in markdown files"
	$(VENV) linkcheckmarkdown README.md docs/*.md

.PHONY: tox
tox:
	@echo "Running tox"
	$(VENV) tox

.PHONY: spellcheck-enchant
spellcheck-enchant:
	@echo "Running spellcheck with pyenchant (via pylint)"
	$(VENV) pylint dedlin --enable C0401,C0402,C0403 --rcfile=.pylintrc_spell

check_spelling:
	$(VENV) pylint dedlin --enable C0402 --rcfile=.pylintrc_spell
	$(VENV) codespell README.md --ignore-words=private_dictionary.txt
	$(VENV) codespell dedlin --ignore-words=private_dictionary.txt

check_changelog:
	# pipx install keepachangelog-manager
	$(VENV) changelogmanager validate

check_all: check_docs check_md check_spelling check_changelog

.PHONY: pipreqs
pipreqs:
	@echo "Running pipreqs"
	$(VENV) pipreqs dedlin --force --print

.PHONY: deptry
deptry:
	@echo "Running deptry"
	$(VENV) deptry .


.PHONY: metadata-sync-check
metadata-sync-check:
	@echo "Checking generated metadata is in sync"
	$(VENV) metametameta sync-check

.PHONY: version-check
version-check:
	@echo "Checking version sources and PyPI ordering"
	$(VENV) metametameta sync-check

.PHONY: dev-status-check
dev-status-check:
	@echo "Verifying Development Status classifier"
	uvx --from troml-dev-status troml-dev-status validate .

.PHONY: gha-validate
gha-validate:
	@echo "Validating GitHub Actions workflows"
	$(VENV) python -c "import pathlib, yaml; [yaml.safe_load(p.read_text(encoding='utf-8')) for p in pathlib.Path('.github/workflows').glob('*.yml')]; print('YAML parse OK')"
	$(VENV) python -c "from pathlib import Path; import yaml; data=yaml.safe_load(Path('.github/workflows/publish_to_pypi.yml').read_text(encoding='utf-8')); build_steps=data['jobs']['build']['steps']; publish_steps=data['jobs']['pypi-publish']['steps']; up=next(s for s in build_steps if s.get('uses','').startswith('actions/upload-artifact@')); down=next(s for s in publish_steps if s.get('uses','').startswith('actions/download-artifact@')); assert up['with']['name']==down['with']['name']=='packages'; assert up['with']['path']==down['with']['path']=='dist/'; print('Artifact handoff OK:', up['uses'], '->', down['uses'])"
	uvx zizmor --no-progress --no-exit-codes .

.PHONY: gha-pin
gha-pin:
	@echo "Pinning GitHub Actions to current SHAs"
	$(VENV) python -c "import os, subprocess, sys; token=os.environ.get('GITHUB_TOKEN') or subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True).stdout.strip(); assert token, 'Set GITHUB_TOKEN or log in with gh auth login'; env=dict(os.environ, GITHUB_TOKEN=token); raise SystemExit(subprocess.run(['gha-update'], env=env).returncode)"

.PHONY: gha-upgrade
gha-upgrade: gha-pin gha-validate
	@echo "GitHub Actions upgrade complete"

check_all_docs: check_docs check_md check_spelling check_changelog

.PHONY: check-all-docs
check-all-docs: check_all_docs

.PHONY: prerelease
prerelease: metadata-sync-check version-check dev-status-check check-all-docs test
	@echo "Pre-release checks complete"

.PHONY: prerelease-llm
prerelease-llm: metadata-sync-check version-check dev-status-check test-llm
	@echo "Quiet pre-release checks complete"
