.PHONY: install-git-hooks
install-git-hooks:
	git config --local core.hooksPath 'git-hooks'

.PHONY: lint
lint: lint-python lint-shell lint-commit-messages

.PHONY: lint-python lint-shell
lint-python lint-shell:
	./$@.sh

.PHONY: lint-commit-messages
lint-commit-messages:
	cz check --rev-range 5addcfffc9b75a7410eb0457be566edee3c3bffb..HEAD

.PHONY: poetry-build
poetry-build:
	cz changelog && poetry build

.PHONY: test
test:
	pytest
