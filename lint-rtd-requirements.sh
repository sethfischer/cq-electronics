#!/usr/bin/env bash

set -o errexit -o noclobber -o nounset

diff --to-file docs/requirements.txt <(poetry export --dev -f requirements.txt)
