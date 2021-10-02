# -*- coding: utf-8 -*-
from idgx.portal import PROJECTNAME
from plone.app.upgrade.utils import loadMigrationProfile
import logging

logger = logging.getLogger(__name__)


def apply_profile(context):
    """ Apply profile v1001 """
    logger.info(__doc__)
    version = 'v1001'
    profile = 'profile-{0}.upgrades.{1}:default'.format(PROJECTNAME, version)
    loadMigrationProfile(context, profile)
