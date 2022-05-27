.PHONY: install-git-hooks
install-git-hooks:
	git config --local core.hooksPath 'git-hooks'

.PHONY: lint
lint: lint-python lint-shell

.PHONY: lint-python lint-shell
lint-python lint-shell:
	./$@.sh
