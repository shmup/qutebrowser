"""Tests for lazy session restore in the WebEngine workaround path."""

import pytest
from unittest.mock import MagicMock
from qutebrowser.qt.core import QUrl
from qutebrowser.browser.browsertab import TabData
from qutebrowser.misc.sessions import TabHistoryItem


@pytest.fixture
def mock_tab():
    tab = MagicMock()
    tab.data = TabData()
    return tab


@pytest.fixture
def history_private(mock_tab):
    from qutebrowser.browser.webengine.webenginetab import WebEngineHistoryPrivate
    hp = object.__new__(WebEngineHistoryPrivate)
    hp._tab = mock_tab
    return hp


class TestLoadItemsWorkaroundLazy:
    """Test that _load_items_workaround defers loading for qute://back URLs."""

    def test_lazy_tab_stores_url_without_loading(self, history_private, mock_tab):
        """A qute://back entry should store the real URL and not call load_url."""
        real_url = QUrl('https://www.youtube.com/watch?v=abc')
        back_url = QUrl('qute://back#YouTube%20Video')

        items = [
            TabHistoryItem(url=real_url, original_url=real_url,
                           title='YouTube Video', active=False),
            TabHistoryItem(url=back_url, original_url=back_url,
                           title='YouTube Video', active=True),
        ]

        history_private._load_items_workaround(items)

        assert mock_tab.data.lazy_url == real_url
        assert mock_tab.data.lazy_title == 'YouTube Video'
        mock_tab.load_url.assert_not_called()

    def test_normal_tab_loads_immediately(self, history_private, mock_tab):
        """A normal (non-lazy) entry should load immediately as before."""
        url = QUrl('https://example.com')

        items = [
            TabHistoryItem(url=url, original_url=url,
                           title='Example', active=True),
        ]

        history_private._load_items_workaround(items)

        assert mock_tab.data.lazy_url is None
        mock_tab.load_url.assert_called_once_with(url)

    def test_lazy_tab_no_previous_entry(self, history_private, mock_tab):
        """qute://back with no previous entry should load qute://back as-is."""
        back_url = QUrl('qute://back#Title')

        items = [
            TabHistoryItem(url=back_url, original_url=back_url,
                           title='Title', active=True),
        ]

        history_private._load_items_workaround(items)

        # No previous entry to defer to, so load qute://back directly
        assert mock_tab.data.lazy_url is None
        mock_tab.load_url.assert_called_once_with(back_url)


class TestLazyLoadOnFocus:
    """Test that focusing a lazy tab triggers loading."""

    def test_focusing_lazy_tab_loads_url(self):
        """When a tab with lazy_url gains focus, load_url should be called."""
        tab = MagicMock()
        tab.data = TabData()
        tab.data.lazy_url = QUrl('https://www.youtube.com/watch?v=abc')
        tab.data.lazy_title = 'YouTube Video'

        browser = MagicMock(spec=['_restoring_session'])
        browser._restoring_session = False

        from qutebrowser.mainwindow.tabbedbrowser import TabbedBrowser
        TabbedBrowser._load_lazy_tab(browser, tab)

        tab.load_url.assert_called_once_with(QUrl('https://www.youtube.com/watch?v=abc'))
        assert tab.data.lazy_url is None
        assert tab.data.lazy_title is None

    def test_focusing_normal_tab_does_nothing(self):
        """When a normal tab gains focus, no extra loading should happen."""
        tab = MagicMock()
        tab.data = TabData()

        browser = MagicMock(spec=['_restoring_session'])
        browser._restoring_session = False

        from qutebrowser.mainwindow.tabbedbrowser import TabbedBrowser
        TabbedBrowser._load_lazy_tab(browser, tab)

        tab.load_url.assert_not_called()


class TestSessionRestoreSuppression:
    """Test that lazy loading is suppressed during session restore."""

    def test_lazy_load_suppressed_during_restore(self):
        """_load_lazy_tab should not load when _restoring_session is True."""
        tab = MagicMock()
        tab.data = TabData()
        tab.data.lazy_url = QUrl('https://www.youtube.com/watch?v=abc')

        browser = MagicMock(spec=['_restoring_session'])
        browser._restoring_session = True

        from qutebrowser.mainwindow.tabbedbrowser import TabbedBrowser
        TabbedBrowser._load_lazy_tab(browser, tab)

        tab.load_url.assert_not_called()
        # lazy_url should still be set — not consumed
        assert tab.data.lazy_url is not None

    def test_lazy_load_allowed_after_restore(self):
        """_load_lazy_tab should work normally when _restoring_session is False."""
        tab = MagicMock()
        tab.data = TabData()
        tab.data.lazy_url = QUrl('https://example.com')
        tab.data.lazy_title = 'Example'

        browser = MagicMock(spec=['_restoring_session'])
        browser._restoring_session = False

        from qutebrowser.mainwindow.tabbedbrowser import TabbedBrowser
        TabbedBrowser._load_lazy_tab(browser, tab)

        tab.load_url.assert_called_once()
        assert tab.data.lazy_url is None


class TestLastTabLazyLoad:
    """Test that the last tab loads even when setCurrentIndex is a no-op."""

    def test_lazy_load_called_explicitly_after_set_current_index(self):
        """When tab_to_focus is already current, _load_lazy_tab should still fire."""
        tab = MagicMock()
        tab.data = TabData()
        tab.data.lazy_url = QUrl('https://example.com')
        tab.data.lazy_title = 'Example'

        browser = MagicMock(spec=['_restoring_session'])
        browser._restoring_session = False

        from qutebrowser.mainwindow.tabbedbrowser import TabbedBrowser
        # first call — simulates what _on_current_changed would do
        TabbedBrowser._load_lazy_tab(browser, tab)
        assert tab.data.lazy_url is None
        tab.load_url.assert_called_once()

        # second call — simulates the explicit safety-net call
        # should be a no-op since lazy_url is already None
        tab.load_url.reset_mock()
        TabbedBrowser._load_lazy_tab(browser, tab)
        tab.load_url.assert_not_called()
