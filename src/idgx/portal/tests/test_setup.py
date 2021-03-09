# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from idgx.portal.testing import IDGX_PORTAL_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that idgx.portal is properly installed."""

    layer = IDGX_PORTAL_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if idgx.portal is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'idgx.portal'))

    def test_browserlayer(self):
        """Test that IIdgxPortalLayer is registered."""
        from idgx.portal.interfaces import (
            IIdgxPortalLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IIdgxPortalLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IDGX_PORTAL_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['idgx.portal'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if idgx.portal is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'idgx.portal'))

    def test_browserlayer_removed(self):
        """Test that IIdgxPortalLayer is removed."""
        from idgx.portal.interfaces import \
            IIdgxPortalLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            IIdgxPortalLayer,
            utils.registered_layers())
