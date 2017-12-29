# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from mareetrad.trader.content.trader import ITrader
from mareetrad.trader.testing import MAREETRAD_TRADER_INTEGRATION_TESTING  # noqa
from zope.component import createObject
from zope.component import queryUtility

import unittest


class TraderIntegrationTest(unittest.TestCase):

    layer = MAREETRAD_TRADER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name='trader')
        schema = fti.lookupSchema()
        self.assertEqual(ITrader, schema)

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name='trader')
        self.assertTrue(fti)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name='trader')
        factory = fti.factory
        obj = createObject(factory)
        self.assertTrue(ITrader.providedBy(obj))

    def test_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='trader',
            id='trader',
        )
        self.assertTrue(ITrader.providedBy(obj))
