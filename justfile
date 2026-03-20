default:
    @just --list

setup:
    uv venv
    uv pip install -r misc/requirements/requirements-pyqt-6.txt --extra-index-url https://www.riverbankcomputing.com/pypi/simple/ --index-strategy unsafe-best-match
    uv pip install -e .

run *args:
    .venv/bin/python -m qutebrowser {{args}}
