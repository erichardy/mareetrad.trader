# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from plone.supermodel import model
from zope.schema import Text
from zope.schema import TextLine
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.app.textfield import RichText
from mareetrad.trader.utils import validateEmail
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
for_trader_txt = u"""
<h2>Vous venez de vous inscrire pour la Marée Trad 2018 !</h2>
<p>Vous avez saisi les éléments ci-dessous :</p>
<p>_trader_description_</p>
<p>Vous serez averti de la suite des événements à partir du 20
mai 2018</p>
<p> </p>
"""


class IMareetradTraderSettings(model.Schema):
    instruments = Text(
        title=_(u'list of research disciplines related with the college'),
        description=_(u'one discipline name per line'),
        default=default_instruments,
        required=True,
        )
    mail_sender = TextLine(
        title=_(u'email adress'),
        description=_(u'required to inform you'),
        constraint=validateEmail,
        default=u'no-reply@maree-trad.net'
        )
    trader_message = RichText(
        title=_(u'message sent to candidate after apply'),
        description=_(u'after apply for candidate'),
        default=for_trader_txt,
        required=False
        )
