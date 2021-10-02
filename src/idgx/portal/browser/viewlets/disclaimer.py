# -*- coding: utf-8 -*-
from idgx.portal.controlpanel import IIDGXSettings
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


class DisclaimerViewlet(ViewletBase):
    """ The disclaimer viewlet """

    def update(self):
        super(DisclaimerViewlet, self).update()
        registry = getUtility(IRegistry)

        try:
            self.settings = registry.forInterface(IIDGXSettings)
        except KeyError:
            pass

    def enabled(self):
        """ Check if the disclaimer has been enabled to be shown """
        if hasattr(self, 'settings'):
            return str(self.settings.disclaimer_enabled).lower()

    def text(self):
        """ Return disclaimer HTML text """
        if hasattr(self, 'settings'):
            return self.settings.disclaimer_text

    def last_modified(self):
        """ Return the timestamp of last time the disclaimer was modified """
        if hasattr(self, 'settings'):
            return self.settings.disclaimer_last_modified
