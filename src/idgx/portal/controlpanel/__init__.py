# -*- coding: utf-8 -*-
from idgx.portal import _
from plone.app.registry.browser import controlpanel
from plone.autoform import directives
from plone.supermodel import model
from zope import schema

DEFAULT_SECTION = _(u'General')


class IIDGXSettings(model.Schema):
    """ Interface for the control panel form.
    """
    directives.widget(available_sections='z3c.form.browser.textlines.TextLinesFieldWidget')
    available_sections = schema.Set(
        title=_(u'Available Sections'),
        description=_(u'List of available sections in the site.'),
        required=True,
        default=set([DEFAULT_SECTION]),
        value_type=schema.TextLine(title=_(u'Section')),
    )

    default_section = schema.Choice(
        title=_(u'Default Section'),
        description=_(u'Section to be used as default on new items.'),
        required=True,
        vocabulary=u'idgx.portal.AvailableSections',
        default=DEFAULT_SECTION,
    )


class IDGXSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IIDGXSettings
    label = _(u'IDGX Settings')
    description = _(u'Here you can modify the settings for idgx.portal.')


class IDGXSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IDGXSettingsEditForm
