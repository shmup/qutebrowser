# qutebrowser

vim-like web browser built on Python and Qt (PyQt6).

## setup

```
just setup
just run
just run --debug --temp-basedir
```

## testing

pytest via tox. run specific tests:

```
tox -e py312 -- tests/unit/browser/test_webelem.py
```

## linting

flake8, pylint, mypy, vulture — all wired through tox:

```
tox -e flake8
tox -e pylint
tox -e mypy-pyqt6
```

## user config

`config.example.py` in this repo IS the live config — it's symlinked to `~/.config/qutebrowser/config.py`. edit it here, `:config-source` (or `<space>rv`) to reload.

- `config.example.py` — main config (aliases, bindings, settings), symlinked in place
- `~/.config/qutebrowser/autoconfig.yml` — auto-saved settings from `:set`
- `~/.config/qutebrowser/quickmarks` — quickmark entries
- `~/.config/qutebrowser/bookmarks/` — bookmarks
- `~/.config/qutebrowser/greasemonkey/` — userscripts (greasemonkey)

## project notes

- python 3.9+, targets 3.10-3.14
- PyQt6 requires riverbankcomputing extra index (handled by justfile)
- entry point: `qutebrowser/__main__.py` → `qutebrowser/qutebrowser.py:main()`
- `--debug --temp-basedir` for isolated dev sessions
- `_foo` convention for unused params (pylint)
