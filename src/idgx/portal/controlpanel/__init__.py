# -*- coding: utf-8 -*-
from idgx.portal import _
from plone import api
from plone.app.registry.browser import controlpanel
from plone.autoform import directives
from plone.supermodel import model
from time import time
from zope import schema
from zope.globalrequest import getRequest
from zope.i18n import translate
from zope.interface import invariant
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


DEFAULT_SECTION = _(u'General')
DEFAULT_DISCLAIMER = (
    u'<p>We use cookies for statistical purposes, '
    u'to make the ads you see more relevant to you, '
    u'to help you sign up for our services, '
    u'or to remember your settings. '
    u'Check our <a>privacy and cookies policy</a>.</p>')


@provider(IContextAwareDefaultFactory)
def timestamp(context):
    """ Return timestamp """
    return translate(
        _('disclaimer_last_modified', default=str(time())),
        context=getRequest())


@provider(IContextAwareDefaultFactory)
def default_disclaimer(context):
    # we need to pass the request as translation context
    return translate(
        _('dislaimer_text', default=DEFAULT_DISCLAIMER),
        context=getRequest())


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

    disclaimer_enabled = schema.Bool(
        title=_(u'dislaimer_enabled', default=u'Enable disclaimer?'),
        description=_(
            u'help_disclaimer',
            default=u'If selected, a disclaimer will be shown the first time a user visits the site',
        ),
        default=False,
    )

    directives.widget('disclaimer_text', klass='pat-tinymce')
    disclaimer_text = schema.Text(
        title=_(u'dislaimer_text', default=u'Disclaimer Text'),
        description=_(
            u'help_disclaimer_text',
            default=u'The text of the disclaimer.',
        ),
        required=True,
        defaultFactory=default_disclaimer,
    )

    directives.mode(disclaimer_last_modified='hidden')
    disclaimer_last_modified = schema.ASCIILine(
        title=_(u'disclaimer_last_modified', default=u'Last modified'),
        description=_(
            u'help_disclaimer_modified',
            default=u'The timestamp of last time the disclaimer was modified.',
        ),
        defaultFactory=timestamp,
    )

    @invariant
    def set_disclaimer_last_modified(data):
        """Store current timestamp on last_modified registry record.
        This invariant is used as a hook to update the timestamp, as
        its code is only executed when the form is saved.
        """
        name = IIDGXSettings.__identifier__ + '.disclaimer_last_modified'
        api.portal.set_registry_record(name, value=str(time()))


class IDGXSettingsEditForm(controlpanel.RegistryEditForm):
    schema = IIDGXSettings
    label = _(u'IDGX Settings')
    description = _(u'Here you can modify the settings for idgx.portal.')


class IDGXSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = IDGXSettingsEditForm
