# -*- coding: utf-8 -*-
"""Behaviours to assign section
"""
from Products.CMFPlone.utils import base_hasattr
from idgx.portal import _
from idgx.portal.utils import section_default_value
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.interfaces import IDexterityContent
from plone.namedfile import field as namedfile
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.component import adapter
from zope.interface import Interface
from zope.interface import provider
import six


class IAltImageMarker(Interface):
    """ Marker interface for objects that have this behavior.
    """


class ISubTitleMarker(Interface):
    """ Marker interface for objects that have this behavior.
    """


class ICopyrightMarker(Interface):
    """ Marker interface for objects that have this behavior.
    """


class ISectionMarker(Interface):
    """ Marker interface for objects that have this behavior.
    """


@provider(IFormFieldProvider)
class IAltImage(model.Schema):
    """Behavior interface to make a content type support alternative image."""

    altimage = namedfile.NamedBlobImage(
        title=_(u'altimage_field_title', default=u'Alternative image'),
        description=_(u'altimage_field_description', default=u''),
        required=False,
    )

    directives.order_after(altimage='ILeadImageBehavior.image_caption')

    directives.no_omit(IEditForm, 'altimage')
    directives.no_omit(IAddForm, 'altimage')


@provider(IFormFieldProvider)
class ICopyright(model.Schema):
    """Behavior interface to make a content type support copyright."""

    copyright = schema.TextLine(
        title=_(u'copyright_field_title', default=u'Copyright'),
        description=_(u'copyright_field_description', default=u''),
        required=False,
    )

    directives.order_before(copyright='ILeadImageBehavior.image_caption')

    directives.no_omit(IEditForm, 'copyright')
    directives.no_omit(IAddForm, 'copyright')


@provider(IFormFieldProvider)
class ISubTitle(model.Schema):
    """Behavior interface to make a content type support sub titles."""

    subtitle = schema.TextLine(
        title=_(u'subtitle_field_title', default=u'Subtitle'),
        description=_(u'subtitle_field_description', default=u'A secondar title of article'),
        required=False
    )

    directives.order_before(subtitle='IDublinCore.title')

    directives.no_omit(IEditForm, 'subtitle')
    directives.no_omit(IAddForm, 'subtitle')


@provider(IFormFieldProvider)
class ISection(model.Schema):
    """Behavior interface to make a content type support sections."""

    section = schema.Choice(
        title=_(u'section_field_title', default=u'Section'),
        description=_(
            u'section_field_description',
            default=u'Named section where the item will appear.',
        ),
        vocabulary=u'idgx.portal.AvailableSections',
        defaultFactory=section_default_value,
    )
    directives.order_before(section='IDublinCore.title')

    directives.widget('section', SelectFieldWidget)
    directives.no_omit(IEditForm, 'section')
    directives.no_omit(IAddForm, 'section')


@adapter(IDexterityContent)
class MetadataBase(object):
    """ This adapter uses DCFieldProperty to store metadata directly on an
        object using the standard CMF DefaultDublinCoreImpl getters and
        setters.
    """

    def __init__(self, context):
        self.context = context


class AltImage(MetadataBase):

    def _get_altimage(self):
        if base_hasattr(self.context, 'altimage'):
            return self.context.altimage
        return None

    def _set_altimage(self, value):
        self.context.altimage = value
    altimage = property(_get_altimage, _set_altimage)


class SubTitle(MetadataBase):

    def _get_subtitle(self):
        return self.context.subtitle

    def _set_subtitle(self, value):
        if not isinstance(value, six.text_type):
            raise ValueError('Subtitle must be text.')
        self.context.subtitle = value
    subtitle = property(_get_subtitle, _set_subtitle)


class Section(MetadataBase):

    def _get_section(self):
        return self.context.section

    def _set_section(self, value):
        self.context.section = value
    section = property(_get_section, _set_section)


class Copyright(MetadataBase):

    def _get_copyright(self):
        return self.context.copyright

    def _set_copyright(self, value):
        if not isinstance(value, six.text_type):
            raise ValueError('Copyright must be text.')
        self.context.copyright = value
    copyright = property(_get_copyright, _set_copyright)
