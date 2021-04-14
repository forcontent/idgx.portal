# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from collective.cover.controlpanel import ICoverSettings
from zope.interface import implementer
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.utils import createContent
from plone.dexterity.utils import createContentInContainer
from zope.i18n.locales import locales
from plone import api


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
            'collective.nitf.upgrades.v1008:default',
            'collective.nitf.upgrades.v2000:default',
            'collective.nitf:default',
            'idgx.portal:uninstall',
            'idgx.portal:initcontent',
            'idgx.temas:default',
            'idgx.temas:uninstall',
            'idgx.tiles:default',
            'idgx.tiles:uninstall',
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
            'plone.restapi:performance',
            'plone.session:default',
            'raptus.autocompletewidget:default',
            'raptus.autocompletewidget:uninstall',
            'webcouturier.dropdownmenu:default',
        ]


def register_tiles(context):
    """ Register tiles and make available for inmediate use.
        FIXME: https://github.com/collective/collective.cover/issues/633
    """
    tiles = [u'collective.nitf', u'albuns']
    remove_tiles = [u'collective.cover.calendar']

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


def _publish(content):
    """Publish the object if it hasn't been published."""
    portal_workflow = api.portal.get_tool('portal_workflow')
    if portal_workflow.getInfoFor(content, 'review_state') != 'published':
        portal_workflow.doActionFor(content, 'publish')
        return True
    return False


def _get_locales_info(portal):
    reg = queryUtility(IRegistry, context=portal)
    language = reg['plone.default_language']
    parts = (language.split('-') + [None, None])[:3]

    try:
        locale = locales.getLocale(*parts)

        # If we get a territory, we enable the combined language codes
        if locale.id.territory:
            return locale.id.language + '_' + locale.id.territory, True, locale
        return locale.id.language, False, locale
    except LoadLocaleError:
        # default to *some* language so we don't error out
        return language, False, locales.getLocale('en')


def import_content(context):
    """Create default content."""
    portal = api.portal.get()
    target_language, is_combined_language, locale = _get_locales_info(portal)
    #create_cover(portal, target_language)
    #create_news_topic(portal, target_language)
    #create_events_topic(portal, target_language)


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
        'collective.nitf',
        'idgx.temas',
        'idgx.tiles',
        'plone.app.imagecropping',
        'webcouturier.dropdownmenu',
    ]

    qi = api.portal.get_tool('portal_quickinstaller')
    for prod_name in uninstall_list:
        if qi.isProductInstalled(prod_name):
            qi.uninstallProducts([prod_name])
