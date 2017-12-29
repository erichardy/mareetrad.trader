# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from mareetrad.trader.testing import MAREETRAD_TRADER_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that mareetrad.trader is properly installed."""

    layer = MAREETRAD_TRADER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if mareetrad.trader is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'mareetrad.trader'))

    def test_browserlayer(self):
        """Test that IMareetradTraderLayer is registered."""
        from mareetrad.trader.interfaces import (
            IMareetradTraderLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IMareetradTraderLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MAREETRAD_TRADER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['mareetrad.trader'])

    def test_product_uninstalled(self):
        """Test if mareetrad.trader is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'mareetrad.trader'))

    def test_browserlayer_removed(self):
        """Test that IMareetradTraderLayer is removed."""
        from mareetrad.trader.interfaces import \
            IMareetradTraderLayer
        from plone.browserlayer import utils
        self.assertNotIn(
           IMareetradTraderLayer,
           utils.registered_layers())
