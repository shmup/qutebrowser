# SPDX-FileCopyrightText: Freya Bruhin (The Compiler) <mail@qutebrowser.org>
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for qutebrowser.mainwindow.windowundo."""

import collections
import dataclasses
from unittest import mock

import pytest

from qutebrowser.qt.core import QByteArray, QObject, pyqtSignal

from qutebrowser.mainwindow import windowundo


@dataclasses.dataclass
class FakeTabbedBrowser:
    """Minimal tabbed browser stub for window undo tests."""

    is_private: bool = False
    undo_stack: collections.deque = dataclasses.field(
        default_factory=lambda: collections.deque()
    )


class FakeWindow:
    """Minimal window stub that provides saveGeometry and tabbed_browser."""

    def __init__(self, geometry=b'fake-geometry', is_private=False,
                 undo_stack=None):
        self._geometry = QByteArray(geometry)
        self.tabbed_browser = FakeTabbedBrowser(
            is_private=is_private,
            undo_stack=undo_stack or collections.deque(),
        )

    def saveGeometry(self):
        return self._geometry


class FakeQApp(QObject):
    """Minimal QApp stub with window_closing signal."""

    window_closing = pyqtSignal(object)


@pytest.fixture
def fake_qapp(qapp):
    """Provide a fake qapp with window_closing signal, patched into objects."""
    app = FakeQApp()
    with mock.patch('qutebrowser.mainwindow.windowundo.objects') as mock_obj:
        mock_obj.qapp = app
        yield app


@pytest.fixture
def undo_manager(fake_qapp, config_stub):
    """Create a WindowUndoManager connected to the fake qapp."""
    config_stub.val.tabs.undo_stack_size = 100
    manager = windowundo.WindowUndoManager()
    return manager


class TestPrivateWindows:

    def test_private_window_not_saved(self, undo_manager, fake_qapp):
        """Closing a private window should not add to the undo stack."""
        window = FakeWindow(is_private=True)
        fake_qapp.window_closing.emit(window)

        with pytest.raises(IndexError):
            undo_manager.undo_last_window_close()

    def test_private_window_skipped_nonprivate_kept(
        self, undo_manager, fake_qapp
    ):
        """A private close between two normal closes shouldn't affect order."""
        win_a = FakeWindow(geometry=b'win-a')
        win_private = FakeWindow(is_private=True, geometry=b'private')
        win_b = FakeWindow(geometry=b'win-b')

        fake_qapp.window_closing.emit(win_a)
        fake_qapp.window_closing.emit(win_private)
        fake_qapp.window_closing.emit(win_b)

        with mock.patch(
            'qutebrowser.mainwindow.windowundo.mainwindow.MainWindow'
        ) as MockMainWindow:
            MockMainWindow.return_value = mock.MagicMock()

            undo_manager.undo_last_window_close()
            MockMainWindow.assert_called_with(
                private=False,
                geometry=QByteArray(b'win-b'),
            )
            undo_manager.undo_last_window_close()
            MockMainWindow.assert_called_with(
                private=False,
                geometry=QByteArray(b'win-a'),
            )


class TestUndoStackSize:

    def test_negative_means_unlimited(
        self, undo_manager, fake_qapp, config_stub
    ):
        """A negative stack size should mean no limit."""
        config_stub.val.tabs.undo_stack_size = -1
        undo_manager._update_undo_stack_size()

        for i in range(50):
            window = FakeWindow(geometry=f'win-{i}'.encode())
            fake_qapp.window_closing.emit(window)

        with mock.patch(
            'qutebrowser.mainwindow.windowundo.mainwindow.MainWindow'
        ) as MockMainWindow:
            MockMainWindow.return_value = mock.MagicMock()

            for _ in range(50):
                undo_manager.undo_last_window_close()

            with pytest.raises(IndexError):
                undo_manager.undo_last_window_close()

    def test_shrinking_stack_evicts(self, undo_manager, fake_qapp, config_stub):
        """Reducing stack size should evict oldest entries."""
        config_stub.val.tabs.undo_stack_size = 100
        undo_manager._update_undo_stack_size()

        for i in range(10):
            window = FakeWindow(geometry=f'win-{i}'.encode())
            fake_qapp.window_closing.emit(window)

        config_stub.val.tabs.undo_stack_size = 2
        undo_manager._update_undo_stack_size()

        with mock.patch(
            'qutebrowser.mainwindow.windowundo.mainwindow.MainWindow'
        ) as MockMainWindow:
            MockMainWindow.return_value = mock.MagicMock()

            undo_manager.undo_last_window_close()
            MockMainWindow.assert_called_with(
                private=False,
                geometry=QByteArray(b'win-9'),
            )
            undo_manager.undo_last_window_close()
            MockMainWindow.assert_called_with(
                private=False,
                geometry=QByteArray(b'win-8'),
            )
            with pytest.raises(IndexError):
                undo_manager.undo_last_window_close()


class TestRestoreFlow:

    def test_restores_geometry_and_tab_stack(self, undo_manager, fake_qapp):
        """Undo should create a window with saved geometry, set its tab
        undo stack, call undo() to restore tabs, and show it."""
        tab_stack = collections.deque(['tab1', 'tab2'])
        window = FakeWindow(geometry=b'saved-geom', undo_stack=tab_stack)
        fake_qapp.window_closing.emit(window)

        with mock.patch(
            'qutebrowser.mainwindow.windowundo.mainwindow.MainWindow'
        ) as MockMainWindow:
            mock_win = mock.MagicMock()
            MockMainWindow.return_value = mock_win

            undo_manager.undo_last_window_close()

            MockMainWindow.assert_called_once_with(
                private=False,
                geometry=QByteArray(b'saved-geom'),
            )
            assert mock_win.tabbed_browser.undo_stack == tab_stack
            mock_win.tabbed_browser.undo.assert_called_once()
            mock_win.show.assert_called_once()
