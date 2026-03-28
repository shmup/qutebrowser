default:
    @just --list

# cross-platform setup

[linux]
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    # system-site-packages picks up system PyQt6/QtWebEngine (has proprietary codecs)
    # use system python so venv matches the python version system packages are built for
    uv venv --system-site-packages --python /bin/python3
    uv pip install -e .
    uv pip install adblock
    echo ""
    echo "setup complete. run with: just run"
    echo "requires system packages: python3-pyqt6 python3-pyqt6-webengine"

[macos]
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    # system-site-packages picks up homebrew PyQt6/QtWebEngine (has proprietary codecs)
    if ! brew list pyqt@6 &>/dev/null || ! brew list qt@6 &>/dev/null; then
        echo "missing homebrew packages. install with:"
        echo "  brew install pyqt@6 qt@6"
        exit 1
    fi
    uv venv --system-site-packages --python /opt/homebrew/bin/python3
    uv pip install -e .
    uv pip install adblock
    echo ""
    echo "setup complete. run with: just run"

[windows]
setup:
    #!powershell
    $ErrorActionPreference = "Stop"
    # pyqt6 from pip on windows includes codecs, so install from riverbank
    uv venv --python python3
    uv pip install -r misc/requirements/requirements-pyqt-6.txt `
        --extra-index-url https://www.riverbankcomputing.com/pypi/simple/ `
        --index-strategy unsafe-best-match
    uv pip install -e .
    uv pip install adblock
    Write-Host ""
    Write-Host "setup complete. run with: just run"

[macos]
run *args:
    QUTE_DISABLE_PAKJOY=1 .venv/bin/python -m qutebrowser {{args}}

[linux]
run *args:
    .venv/bin/python -m qutebrowser {{args}}

[windows]
run *args:
    .venv\Scripts\python.exe -m qutebrowser {{args}}

[unix]
test *args:
    .venv/bin/python -m pytest tests/unit {{args}}

[windows]
test *args:
    .venv\Scripts\python.exe -m pytest tests\unit {{args}}

# install macos .app bundle to ~/Applications
[macos]
install-app:
    #!/usr/bin/env bash
    set -euo pipefail
    dest="$HOME/Applications/qutebrowser-dev.app"
    rsync -a --delete misc/macos/qutebrowser-dev.app/ "$dest/"
    cp qutebrowser/icons/qutebrowser.icns "$dest/Contents/Resources/"
    chmod +x "$dest/Contents/MacOS/launch"
    /System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -f "$dest"
    echo "installed $dest and registered with launch services"
    echo "qutebrowser-dev should now appear in Desktop & Dock > Default web browser"
