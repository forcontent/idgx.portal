# -*- coding: utf-8 -*-
from collective.nitf.interfaces import INITF
from collective.nitf.content import NITF
from zope.interface import implementer


@implementer(INITF)
class NITF(NITF):
    def getField(self, name):
        if 'image' in name:
            return self.unrestrictedTraverse('@@images')
        return self.get(name, None)
