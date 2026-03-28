default:
    @just --list

# cross-platform setup using uv inline scripts

[unix]
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    uv venv
    # pyqt6 is hosted on riverbank's private pypi, not the main one
    uv pip install -r misc/requirements/requirements-pyqt-6.txt \
        --extra-index-url https://www.riverbankcomputing.com/pypi/simple/ \
        --index-strategy unsafe-best-match
    uv pip install -e .
    uv pip install adblock
    echo ""
    echo "setup complete. run with: just run"

[windows]
setup:
    #!powershell
    $ErrorActionPreference = "Stop"
    uv venv
    # pyqt6 is hosted on riverbank's private pypi, not the main one
    uv pip install -r misc/requirements/requirements-pyqt-6.txt `
        --extra-index-url https://www.riverbankcomputing.com/pypi/simple/ `
        --index-strategy unsafe-best-match
    uv pip install -e .
    uv pip install adblock
    Write-Host ""
    Write-Host "setup complete. run with: just run"

[unix]
run *args:
    .venv/bin/python -m qutebrowser {{args}}

[windows]
run *args:
    .venv\Scripts\python.exe -m qutebrowser {{args}}
