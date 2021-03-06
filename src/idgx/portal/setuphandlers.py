# -*- coding: utf-8 -*-
from collective.cover.controlpanel import ICoverSettings
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'Products.CMFPlacefulWorkflow:base',
            'collective.cover:default',
            'collective.easyform:default',
            'collective.easyform:uninstall',
            'collective.fingerpointing:default',
            'collective.js.galleria:default',
            'collective.js.jqueryui:default',
            'idgx.portal:initcontent',
            'idgx.portal:uninstall',
            'idgx.temas:default',
            'idgx.temas:uninstall',
            'plone.app.blocks:default',
            'plone.app.contenttypes:default',
            'plone.app.contenttypes:plone-content',
            'plone.app.dexterity:default',
            'plone.app.imagecropping:default',
            'plone.app.imagecropping:uninstall',
            'plone.app.iterate:plone.app.iterate',
            'plone.app.jquerytools:default',
            'plone.app.multilingual:default',
            'plone.app.querystring:default',
            'plone.app.referenceablebehavior:default',
            'plone.app.relationfield:default',
            'plone.app.tiles:default',
            'plone.formwidget.contenttree:default',
            'plone.formwidget.contenttree:uninstall',
            'plone.microsite:default',
            'plone.microsite:uninstall',
            'plone.restapi:performance',
            'plone.session:default',
            'raptus.autocompletewidget:default',
            'raptus.autocompletewidget:uninstall',
            'webcouturier.dropdownmenu:default',
        ]


def register_tiles(context):
    """
    """
    tiles = [u'idgx.portal.basic']
    remove_tiles = [u'collective.cover.calendar', u'collective.cover.basic']

    record_tiles = dict(name='plone.app.tiles')
    record_availables = dict(interface=ICoverSettings, name='available_tiles')

    registered_tiles = api.portal.get_registry_record(**record_tiles)
    available_tiles = api.portal.get_registry_record(**record_availables)

    for tile in remove_tiles:
        if tile in registered_tiles:
            registered_tiles.remove(tile)
            available_tiles.remove(tile)

    for tile in tiles:
        if tile not in registered_tiles:
            registered_tiles.append(tile)

    for tile in tiles:
        if tile not in available_tiles:
            available_tiles.append(tile)

    api.portal.set_registry_record(value=registered_tiles, **record_tiles)
    api.portal.set_registry_record(value=available_tiles, **record_availables)


def post_install(context):
    """Post install script"""
    register_tiles(context)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
    uninstall_list = [
        'collective.cover',
        'collective.easyform',
        'collective.fingerpointing',
        'collective.js.galleria',
        'idgx.temas',
        'plone.app.imagecropping',
        'plone.microsite',
        'webcouturier.dropdownmenu',
    ]

    qi = api.portal.get_tool('portal_quickinstaller')
    for prod_name in uninstall_list:
        if qi.isProductInstalled(prod_name):
            qi.uninstallProducts([prod_name])
