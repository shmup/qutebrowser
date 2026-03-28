"""On-disk favicon cache keyed by URL host.

Saves favicons as PNGs so they can be restored on session load
before the page has loaded (e.g. for pinned or lazy tabs).
"""

import hashlib
import os
from typing import Optional

from qutebrowser.qt.core import QUrl, QByteArray, QBuffer, QIODevice
from qutebrowser.qt.gui import QIcon, QPixmap

from qutebrowser.utils import standarddir, log


def _cache_dir() -> str:
    return os.path.join(standarddir.data(), 'favicons')


def _key_for_url(url: QUrl) -> Optional[str]:
    """Return a cache key for the given URL, or None if not cacheable."""
    host = url.host()
    if not host:
        return None
    return hashlib.sha1(host.encode('utf-8')).hexdigest()[:16]


def _path_for_url(url: QUrl) -> Optional[str]:
    key = _key_for_url(url)
    if key is None:
        return None
    return os.path.join(_cache_dir(), f'{key}.png')


def save(url: QUrl, icon: QIcon) -> None:
    """Save a favicon to disk for the given URL."""
    path = _path_for_url(url)
    if path is None:
        return

    pixmap = icon.pixmap(32, 32)
    if pixmap.isNull():
        return

    cache_dir = _cache_dir()
    os.makedirs(cache_dir, exist_ok=True)

    buf = QByteArray()
    buffer = QBuffer(buf)
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    pixmap.save(buffer, 'PNG')
    buffer.close()

    try:
        with open(path, 'wb') as f:
            f.write(bytes(buf))
    except OSError:
        log.misc.debug(f'Failed to save favicon for {url.host()}')


def load(url: QUrl) -> Optional[QIcon]:
    """Load a cached favicon for the given URL, or None if not cached."""
    path = _path_for_url(url)
    if path is None:
        return None

    if not os.path.exists(path):
        return None

    pixmap = QPixmap()
    if not pixmap.load(path):
        return None

    return QIcon(pixmap)
