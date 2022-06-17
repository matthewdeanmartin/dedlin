#!/usr/bin/env bash
set -euo pipefail
mypy dedlin
pylint dedlin
pytest test
