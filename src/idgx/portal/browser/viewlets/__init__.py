# -*- coding: utf-8 -*-
from idgx.portal.behaviors.metadata import IAltImage
from idgx.portal.behaviors.metadata import ICopyright
from idgx.portal.behaviors.metadata import ISection
from idgx.portal.behaviors.metadata import ISubTitle
from plone.app.layout.viewlets import ViewletBase


class AltImageViewlet(ViewletBase):
    """ A simple viewlet which renders altimage """

    def update(self):
        context = IAltImage(self.context)
        self.available = True if context.altimage else False


class CopyrightViewlet(ViewletBase):
    """ A simple viewlet which renders copyright """

    def update(self):
        context = ICopyright(self.context)
        self.available = True if context.copyright else False


class SubTitleViewlet(ViewletBase):
    """ A simple viewlet which renders subtitle """

    def update(self):
        context = ISubTitle(self.context)
        self.available = True if context.subtitle else False


class SectionViewlet(ViewletBase):
    """ A simple viewlet which renders section """

    def update(self):
        context = ISection(self.context)
        self.available = True if context.section else False
