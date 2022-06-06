.PHONY: install-git-hooks
install-git-hooks:
	git config --local core.hooksPath 'git-hooks'

.PHONY: lint
lint: lint-python lint-shell lint-rtd-requirements

.PHONY: lint-python lint-shell lint-rtd-requirements
lint-python lint-shell lint-rtd-requirements:
	./$@.sh

.PHONY: poetry-build
poetry-build:
	cz changelog && poetry build
