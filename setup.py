# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup


version = '3.0a1'
long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CONTRIBUTORS.rst').read(),
    open('CHANGES.rst').read(),
])
entry_point = 'idgx.portal:Recipe'

setup(
    name='idgx.portal',
    version=version,
    description="Implementação Modelo da Identidade Digital de Governo",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Plone :: 5.2",
        "Framework :: Plone :: Addon",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Multimedia",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='Python Plone CMS IDGX .gov.br identidade_digital egov',
    author='ForContent',
    author_email='suporte@forcontent.com.br',
    url='https://github.com/forcontent/idgx.portal',
    project_urls={
        'PyPI': 'https://pypi.python.org/pypi/idgx.portal',
        'Source': 'https://github.com/collective/idgx.portal',
        'Tracker': 'https://github.com/collective/idgx.portal/issues',
        # 'Documentation': 'https://idgx.portal.readthedocs.io/en/latest/',
    },
    license='GPL version 2',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['idgx'],
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    python_requires="==2.7, >=3.8",
    install_requires=[
        'setuptools',
        # -*- Extra requirements: -*-
        'collective.cover',
        'collective.easyform',
        'collective.fingerpointing',
        'collective.nitf',
        'idgx.temas',
        'plone.api>=1.8.4',
        'plone.app.dexterity',
        'plone.restapi',
        'sc.social.like',
        'z3c.jbot',
    ],
    extras_require={
        'migration': [
            'collective.jsonmigrator',
            'collective.transmogrifier',
            'plone.app.transmogrifier',
            'transmogrify.dexterity',
        ],
        'test': [
            'plone.app.testing',
            # Plone KGS does not use this version, because it would break
            # Remove if your package shall be part of coredev.
            # plone_coredev tests as of 2016-04-01.
            'plone.app.contenttypes',
            'plone.app.robotframework[debug]',
            'plone.app.testing [robot]',
            'plone.testing>=5.0.0',
        ],
    },
    entry_points = {
        'zc.buildout': ['default = {0:s}'.format(entry_point)],
        'z3c.autoinclude.plugin': ['target = plone'],
        'console_scripts': ['update_locale = idgx.portal.locales.update:update_locale'],
    }
)
