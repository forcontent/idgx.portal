# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from Products.CMFPlone.utils import _createObjectByType
from datetime import datetime
from io import BytesIO
from plone import api
from plone.app.dexterity.behaviors import constrains
from plone.app.textfield.value import RichTextValue
from plone.dexterity.utils import addContentToContainer
from plone.dexterity.utils import createContent
from plone.dexterity.utils import createContentInContainer
from plone.i18n.normalizer import idnormalizer
from plone.locking.interfaces import ILockable
from plone.namedfile.file import NamedBlobImage
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
from zope.i18n.interfaces import ITranslationDomain
from zope.i18n.locales import locales

import base64
import glob
import json
import os
import re


def _translate(name, target_language, default=u''):
    """Simple function to translate a string."""
    result = None
    if target_language != 'en':
        util = queryUtility(ITranslationDomain, 'idgx.portal')
        if util is not None:
            result = util.translate(name, target_language=target_language,
                                    default=default)
    return result and result or default


def _publish(content):
    """Publish the object if it hasn't been published."""
    portal_workflow = api.portal.get_tool('portal_workflow')
    if portal_workflow.getInfoFor(content, 'review_state') != 'published':
        portal_workflow.doActionFor(content, 'publish')
        return True
    return False


def _setup_constrains(container, allowed_types):
    behavior = ISelectableConstrainTypes(container)
    behavior.setConstrainTypesMode(constrains.ENABLED)
    behavior.setImmediatelyAddableTypes(allowed_types)
    return True


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


def cleaning_house(portal):
    """ Removing default objects of Plone """
    rm_ids = ['front-page', 'news', 'events', 'noticias', 'eventos', 'home',
            'pagina-inicial']
    remove_list = [obj_id for obj_id in rm_ids if obj_id in portal.keys()]

    if len(remove_list) > 0:
        for obj_id in remove_list:
            obj = portal[obj_id]

            if not 'Folder' in obj.portal_type:
                lockable = ILockable(portal[obj_id])

                if lockable.locked():
                    lockable.unlock()
        portal.manage_delObjects(remove_list)


def create_topic(portal, target_language):
    news_id = idnormalizer.normalize(_translate(u'news-title', target_language,
        u'News'))

    #images_id = idnormalizer.normalize(_translate(u'images-title', target_language,
    #    u'Images'))

    if news_id not in portal.keys():
        title = _translate(u'news-title', target_language, u'News')
        description = _translate(u'news-description', target_language,
                                 u'Site News')
        container = createContent(
            'Folder', id=news_id,
            title=title,
            description=description,
            language=target_language.replace('_', '-').lower())
        container = addContentToContainer(portal, container)

        collection_id = idnormalizer.normalize(_translate(u'list-title',
            target_language, u'List'))
        _createObjectByType('Collection', container,
                            id=collection_id, title=title,
                            description=description)
        aggregator = container[collection_id]

        # Constrain types
        allowed_types = ['News Item', ]
        _setup_constrains(container, allowed_types)

        container.setOrdering('unordered')
        container.setDefaultPage(collection_id)
        _publish(container)

        # Set the Collection criteria.
        #: Sort on the Effective date
        aggregator.sort_on = u'effective'
        aggregator.sort_reversed = True
        #: Query by Type and Review State
        aggregator.query = [
            {'i': u'portal_type',
             'o': u'plone.app.querystring.operation.selection.any',
             'v': [u'News Item'],
             },
            {'i': u'review_state',
             'o': u'plone.app.querystring.operation.selection.any',
             'v': [u'published'],
             },
        ]
        aggregator.setLayout('tabular_view')
        _publish(aggregator)


    #if images_id not in portal.keys():
    #    title = _translate(u'images-title', target_language, u'Images')
    #    description = _translate(u'images-description', target_language,
    #                             u'Images folder')
    #    container = createContent(
    #        'Folder', id=images_id,
    #        title=title,
    #        description=description,
    #        language=target_language.replace('_', '-').lower())
    #    container = addContentToContainer(portal, container)

    #    imgs_collection_id = idnormalizer.normalize(_translate(u'list-title',
    #        target_language, u'List'))
    #    _createObjectByType('Collection', container,
    #                        id=imgs_collection_id, title=title,
    #                        description=description)
    #    aggregator = container[imgs_collection_id]

    #    # Constrain types
    #    allowed_types = ['Image', ]
    #    _setup_constrains(container, allowed_types)

    #    container.setOrdering('unordered')
    #    container.setDefaultPage(imgs_collection_id)
    #    _publish(container)

    #    # Set the Collection criteria.
    #    #: Sort on the Effective date
    #    aggregator.sort_on = u'effective'
    #    aggregator.sort_reversed = True
    #    #: Query by Type and Review State
    #    aggregator.query = [
    #        {'i': u'portal_type',
    #         'o': u'plone.app.querystring.operation.selection.any',
    #         'v': [u'Image'],
    #         },
    #    ]
    #    aggregator.setLayout('tabular_view')
    #    _publish(aggregator)


def read_directory(directory):
        data_file = 'data.json'
        children_file = 'children.json'

        path = '{0}/{1}'.format(directory, data_file)
        try:
            data = json.loads(open(path, 'r').read())
        except IOError:
            # Arquivo data.json não existe
            data = {}
        except ValueError:
            # json mal formado
            data = {}

        yield data

        path = '{0}/{1}'.format(directory, children_file)
        try:
            children = json.loads(open(path, 'r').read())
        except IOError:
            # Arquivo children.json não existe.
            children = []
        except ValueError:
            # json mal formado
            children = []
        for child in children:
            oId = child.get('id')
            path = '%s/%s' % (directory, oId)
            for item in read_directory(path):
                yield item


def datetime_to_integer(dt_time):
    dt = datetime.strptime(dt_time, '%Y-%m-%d %H:%M:%S')
    return 10000*dt.year + 100*dt.month + dt.day


def dummy_image(filename=u'image.jpg', b64=None):
    if b64:
        im = BytesIO(base64.b64decode( re.sub("data:image/jpeg;base64", '', b64) ))
        image_data = im.read()
    else:
        filename = os.path.join(os.path.dirname(__file__), filename)
        with open(filename, 'rb') as f_img:
            image_data = f_img.read()

    return NamedBlobImage(
        data=image_data,
        filename=filename
    )


def create_newsitem(portal, target_language):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    news_id = idnormalizer.normalize(_translate(u'news-title', target_language,
        u'News'))
    path_to_json = glob.glob('{}/json/**'.format(dir_path))

    if news_id in portal.keys():
        container = portal[news_id]

        for jpath in path_to_json:
            for item in read_directory(jpath):

                if item.get('_path'):
                    item['_path'] = "{}/{}".format(portal.id, item['_path'])

                    if item['_type'] == 'News Item':

                        if item.get('effective'):
                            item['effective'] = datetime_to_integer(item['effective'])

                        img = item.get('_datafield_image', None)

                        if img:
                            del item['_datafield_image']

                        content = createContent(
                            item['_type'], id=item['_id'],
                            language=target_language.replace('_', '-').lower(), **item)
                        content = addContentToContainer(container, content)
                        content.text = RichTextValue(
                            item['text'],
                            'text/html',
                            'text/x-html-safe'
                        )

                        if img:
                            content.image = dummy_image(filename=img['filename'], b64=img['data'])

                            if img.get('copyright'):
                                content.copyright = img['copyright']

                        _publish(content)
                        content.reindexObject()


def create_images(portal, target_language):

    dir_path = os.path.dirname(os.path.realpath(__file__))
    images_id = idnormalizer.normalize(_translate(u'images-title', target_language,
        u'Images'))
    path_to_json = glob.glob('{}/json/**'.format(dir_path))

    if images_id in portal.keys():
        container = portal[images_id]

        for jpath in path_to_json:
            for item in read_directory(jpath):

                    if item['_type'] == 'Image':
                        img_data = item['_datafield_image']
                        content = createContent(
                            item['_type'], id=item['_id'],
                            language=target_language.replace('_', '-').lower(), **item)
                        #pth = os.path.basename(item['_path'].strip('{}'.format(item['_id'])))
                        pth = item['_path'].rstrip('{}'.format(item['_id']))
                        content = addContentToContainer(container.unrestrictedTraverse(pth), content)

                        content.image = dummy_image(filename=img_data['filename'], b64=img_data['data'])
                        content.reindexObject()


def create_cover(portal, target_language):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    news_id = idnormalizer.normalize(_translate(u'news-title', target_language,
        u'News'))
    collection_id = idnormalizer.normalize(_translate(u'list-title',
            target_language, u'List'))
    cover_id = idnormalizer.normalize(_translate(u'initial-page', target_language,
        u'Home'))
    path_to_json = glob.glob('{}/json/**'.format(dir_path))

    if cover_id not in portal.keys():
        container = portal
        content_container = portal[news_id]

        for jpath in path_to_json:
            for item in read_directory(jpath):

                if item['_type'] == 'collective.cover.content':

                    if item.get('effective'):
                        item['effective'] = datetime_to_integer(item['effective'])

                    content = createContent(
                        item['_type'], id=item['_id'],
                        language=target_language.replace('_', '-').lower(), **item)
                    content = addContentToContainer(container, content)

                    contents = [{'tile': 'c2e54572-5f53-4d53-ae57-29a2354f663e', 'content': 'noticia-de-exemplo-4'},
                                {'tile': 'bef3a69c-df38-4763-80df-ec57f03db3d1', 'content': 'noticia-de-exemplo-1'},
                                {'tile': 'facfd146-f324-4cc5-bbfc-9d8113947291', 'content': 'noticia-de-exemplo-5'},
                                {'tile': 'fa84c576-0795-49c8-a596-5cbd2260d210', 'content': 'noticia-de-exemplo-3'},
                                {'tile': 'c236aeb0-d651-4f99-b325-4cb5d1bf5d74', 'content': 'noticia-de-exemplo-4',}]

                    for tile_content in contents:
                        content.get_tile(tile_content['tile']).populate_with_object(content_container[tile_content['content']])
                    _publish(content)
                    content.reindexObject()

        if not hasattr(portal, 'default_page'):
            portal.manage_addProperty('default_page',
                                      cover_id, 'string')



def import_content(context):
    """Create default content."""
    portal = api.portal.get()
    cleaning_house(portal)
    target_language, is_combined_language, locale = _get_locales_info(portal)
    create_topic(portal, target_language)
    create_newsitem(portal, target_language)
    create_cover(portal, target_language)
