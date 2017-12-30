# -*- coding: utf-8 -*-

from plone import api
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
from AccessControl import getSecurityManager
import logging
from mareetrad.trader.utils import validateEmail
from mareetrad.trader.utils import setUnsecure
from mareetrad.trader.utils import setSecure
from mareetrad.trader.utils import sorted_by_date
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
    sender_registration = schema.TextLine(
        title=_(u'mail_sender for registration confirm'),
        description=_(u'email adress of the mail registration sender'),
        default=u'no-reply@maree-trad.net',
        constraint=validateEmail
        )
    mails_activated = schema.Bool(
        title=_(u'activate mails for this Maree Trad'),
        description=_(u'unselect to de-activate mails'),
        default=True
        )
    before = RichText(
        title=_(u'text before the traders list'),
        required=False
        )
    after = RichText(
        title=_(u'text after the traders list'),
        required=False
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
    def getTraders(self, byDate=False):
        sm = getSecurityManager()
        setUnsecure(sm)
        traders_found = api.content.find(
            context=self,
            portal_type='trader',
            )
        traders = [t.getObject() for t in traders_found]
        setSecure(sm)
        if byDate:
            return sorted(traders, sorted_by_date)
        return traders


class View(BrowserView):
    pass
