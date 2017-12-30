# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone.supermodel import model
from zope.schema import Text
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from mareetrad.trader import _


class IMareetradTraderLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


default_instruments = u"""Accordéon diatonique Sol/Do
Accordéon Chromatique
Violon
Guitare
Flute traversière
Flûte à bec
Thin whisle
Concertina système Anglo
Concertina système English
Autre
"""


class IMareetradTraderSettings(model.Schema):
    instruments = Text(
        title=_(u'list of instruments'),
        description=_(u'one instrument name per line'),
        default=default_instruments,
        required=True,
        )
