# -*- coding: utf-8 -*-

# from plone import api
import datetime
from plone.dexterity.content import Container
from plone.app.textfield import RichText

from plone.supermodel import model
from Products.Five import BrowserView
from zope import schema
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory
from collective import dexteritytextindexer

import logging
from mareetrad.trader.utils import validateEmail
from mareetrad.trader import _

logger = logging.getLogger('mareetrad.trader:trader')

for_trader_txt = u"""
<h2>Vous venez de vous inscrire pour la Marée Trad 2018</h2>
<p>Vous avez saisi les éléments ci-dessous :</p>
<p>_trader_description_</p>
<p>Vous serez averti de la suite des événements plus tard</p>
<p> </p>
"""


@provider(IContextAwareDefaultFactory)
def registerDate(context):
    return datetime.datetime.today()


class IMareeTraders(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Trader
    """

    dexteritytextindexer.searchable('mail_sender')
    mail_sender = schema.TextLine(
        title=_(u'mail_sender'),
        description=_(u'email adress of the mails sender'),
        default=u'aze.qsd@poi.fr',
        constraint=validateEmail
        )
    mails_activated = schema.Bool(
        title=_(u'activate mails for this Maree Trad'),
        description=_(u'unselect to de-activate mails'),
        default=True
        )
    for_traders = RichText(
        title=_(u'message sent to traders after register'),
        description=_(u'macro _trader_description_'),
        default=for_trader_txt,
        required=False
        )


@implementer(IMareeTraders)
class mareeTraders(Container):
    """
    """


class View(BrowserView):
    pass
