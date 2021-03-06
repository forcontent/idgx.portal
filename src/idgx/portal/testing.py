# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import idgx.portal


class IdgxPortalLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=idgx.portal)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'idgx.portal:default')


IDGX_PORTAL_FIXTURE = IdgxPortalLayer()


IDGX_PORTAL_INTEGRATION_TESTING = IntegrationTesting(
    bases=(IDGX_PORTAL_FIXTURE,),
    name='IdgxPortalLayer:IntegrationTesting',
)


IDGX_PORTAL_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(IDGX_PORTAL_FIXTURE,),
    name='IdgxPortalLayer:FunctionalTesting',
)


IDGX_PORTAL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        IDGX_PORTAL_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='IdgxPortalLayer:AcceptanceTesting',
)
