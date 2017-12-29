# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import mareetrad.trader


class MareetradTraderLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=mareetrad.trader)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'mareetrad.trader:default')


MAREETRAD_TRADER_FIXTURE = MareetradTraderLayer()


MAREETRAD_TRADER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MAREETRAD_TRADER_FIXTURE,),
    name='MareetradTraderLayer:IntegrationTesting'
)


MAREETRAD_TRADER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MAREETRAD_TRADER_FIXTURE,),
    name='MareetradTraderLayer:FunctionalTesting'
)


MAREETRAD_TRADER_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MAREETRAD_TRADER_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='MareetradTraderLayer:AcceptanceTesting'
)
