# -*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from collective.cover.logger import logger
from collective.cover.tiles.basic import BasicTile
from collective.cover.tiles.basic import IBasicTile
from collective.cover.tiles.configuration_view import IDefaultConfigureForm
from idgx.portal import _
from plone.autoform import directives
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from zope import schema
from zope.browserpage import ViewPageTemplateFile
from zope.interface import implementer


class IIdgxBasicTile(IBasicTile):

    """A tile that shows information about a News Article."""

    subtitle = schema.TextLine(
        title=_(u'Subtitle'),
        required=False,
    )

    directives.omitted('section')
    directives.no_omit(IDefaultConfigureForm, 'section')
    section = schema.TextLine(
        title=_(u'Section'),
        required=False,
    )

    media_producer = schema.TextLine(
        title=_(u'Image Rights'),
        required=False,
    )


@implementer(IIdgxBasicTile)
class IdgxBasicTile(BasicTile):

    """A tile that shows information about a News Article."""

    index = ViewPageTemplateFile('templates/idgxbasic_tile.pt')
    is_configurable = True
    is_editable = True
    is_droppable = True

    short_name = _(u'msg_short_name_basic', default=u'Basic')

    def populate_with_object(self, obj):
        super(BasicTile, self).populate_with_object(obj)

        title = safe_unicode(obj.Title())
        description = safe_unicode(obj.Description())

        image = self.get_image_data(obj)
        if image:
            # clear scales if new image is getting saved
            self.clear_scales()

        # initialize the tile with all fields needed for its rendering
        # note that we include here 'date' and 'subjects', but we do not
        # really care about their value: they came directly from the catalog
        # brain
        data = {
            'title': title,
            'description': description,
            'subtitle': obj.subtitle or '',
            'section' : obj.section or '',
            'uuid': IUUID(obj),
            'date': True,
            'subjects': True,
            'image': image,
            'alt_text': description or title,
            'media_producer' : obj.copyright or '',
        }

        data_mgr = ITileDataManager(self)
        data_mgr.set(data)

        msg = 'tile "{0}"" populated with data: {1}'
        logger.debug(msg.format(self.id, data))


    def _get_field_configuration(self, field):
        """Return a dict with the configuration of the field. This is a
        helper function to deal with the ugliness of the internal data
        structure.
        """
        fields = self.get_configured_fields()
        return [f for f in fields if f['id'] == field][0]

    @property
    def title_tag(self):
        field = self._get_field_configuration('title')
        tag, title, href = field['htmltag'], field['content'], self.getURL()
        if href:
            return u'<{tag}><a href="{href}">{title}</a></{tag}>'.format(
                tag=tag, href=href, title=title)
        else:
            # in HTML5 the href attribute may be omitted (placeholder link)
            return u'<{tag}><a>{title}</a></{tag}>'.format(tag=tag, title=title)
