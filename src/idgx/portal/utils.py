# -*- coding: utf-8 -*-
from idgx.portal.controlpanel import IIDGXSettings
from plone import api


def section_default_value():
    """Return the default value for the section field as defined in
    the control panel configlet.
    """
    record = IIDGXSettings.__identifier__ + '.default_section'
    return api.portal.get_registry_record(record)
