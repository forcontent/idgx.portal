#-*- coding: utf-8 -*-
from idgx.portal import _
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.schema.vocabulary import SimpleVocabulary
from idgx.portal.controlpanel import IIDGXSettings


def _normalize_token(token):
    """Normalize a token using ascii as encoding."""
    normalizer = getUtility(IIDNormalizer)

    return normalizer.normalize(token).lower()


def SectionsVocabulary(context):
    """ Creates a vocabulary with the available sections stored in the
    registry; the vocabulary is normalized to allow the use of non-ASCII
    characters.
    """
    registry = getUtility(IRegistry)
    settings = registry.forInterface(IIDGXSettings)
    available_sections = list(settings.available_sections)
    available_sections.sort()
    items = []
    for section in available_sections:
        token = _normalize_token(section)
        items.append(SimpleVocabulary.createTerm(section, token, section))
    return SimpleVocabulary(items)
