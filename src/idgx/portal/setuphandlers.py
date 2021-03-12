# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
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
            'plone.app.blocks:default',
            'plone.app.contenttypes:default',
            'plone.app.contenttypes:plone-content',
            'plone.app.dexterity:default',
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
            'sc.social.like:default',
        ]


def add_content_central_menu():
    """Add Content Central menu option to Folder content type."""
    view = 'centrais-de-conteudo'
    folder_fti = api.portal.get_tool('portal_types')['Folder']
    folder_fti.view_methods += (view,)
    assert view in folder_fti.view_methods  # nosec


def set_social_media_settings():
    """Update configuration of sc.social.like package."""
    name = 'sc.social.like.interfaces.ISocialLikeSettings.enabled_portal_types'
    value = (
        'collective.cover.content',
        'collective.nitf.content',
        'Document',
        'Event',
        'Image',
    )
    api.portal.set_registry_record(name, value)


def add_results_filter_menu():
    """Add Results Filter menu option to Collection content type."""
    view = 'filtro-de-resultados'
    collection_fti = api.portal.get_tool('portal_types')['Collection']
    collection_fti.view_methods += (view,)
    assert view in collection_fti.view_methods  # nosec


def post_install(context):
    """Post install script"""
    set_social_media_settings()
    add_content_central_menu()
    add_results_filter_menu()


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.
