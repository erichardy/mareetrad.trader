# -*- coding: utf-8 -*-

from plone import api
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.dexterity.browser import add

from plone.supermodel import model
from Products.Five import BrowserView
from z3c.form import button
from zope import schema
from zope.interface import implementer
from collective import dexteritytextindexer

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import (
    newSecurityManager, setSecurityManager)
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
# from plone.protect.utils import addTokenToUrl

import logging
from mareetrad.trader.utils import validateEmail
from mareetrad.trader import _

logger = logging.getLogger('mareetrad.trader:trader')


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return 'AnonymousTrader'


class ITrader(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Trader
    """
    dexteritytextindexer.searchable('name')
    model.primary('name')
    name = schema.TextLine(
        title=_(u'trader name'),
        description=_(u'your family name'),
        default=u'Nomm',
        )
    dexteritytextindexer.searchable('firstname')
    firstname = schema.TextLine(
        title=_(u'trader firstame'),
        description=_(u'your first name'),
        default=u'Prééénomm',
        )
    dexteritytextindexer.searchable('town')
    town = schema.TextLine(
        title=_(u'the town where you live'),
        description=_(u''),
        required=False,
        )
    age = schema.Int(
        title=_(u'your age'),
        description=_(u'how old are you'),
        min=1,
        max=110,
        default=33,
        )
    mobile = schema.TextLine(
        title=_(u'mobile phone number'),
        description=_(u'required to inform you'),
        default=u'123123123',
        )
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'email adress'),
        description=_(u'required to inform you'),
        constraint=validateEmail,
        default=u'aze.qsd@poi.fr'
        )
    intrument = schema.Choice(
        title=_(u'intrument played at the maree trad'),
        description=_(u'if your intrument is not there, choose "Other"'),
        source='trader.instruments',
        default=u'',
        required=True,
        )
    other_instrument = schema.TextLine(
        title=_(u'intrument played'),
        description=_(u'if your intrument is not in the list above'),
        required=False,
        )
    form.omitted('register_date')
    register_date = schema.Date(
        title=_(u'registring date'),
        required=False,
        )


@implementer(ITrader)
class Trader(Item):
    """
    """


class View(BrowserView):
    pass


class AddForm(add.DefaultAddForm):
    portal_type = 'trader'
    ignoreContext = True
    label = _(u'register a new trader !')

    def update(self):
        super(add.DefaultAddForm, self).update()
        # import pdb;pdb.set_trace()

    def updateWidgets(self):
        super(add.DefaultAddForm, self).updateWidgets()

    @button.buttonAndHandler(_(u'Register'), name='register')
    def handleApply(self, action):
        portal = api.portal.get()
        sm = getSecurityManager()
        data, errors = self.extractData()
        if errors:
            self.status = _('Please correct errors')
            return
        try:
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(), '', ['Manager'], '')
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)
            obj = self.createAndAdd(data)
            uuid = api.content.get_uuid(obj=obj)
            # context is now the thesis repo
            # repo = obj.__of__(self.context)
            url = portal.absolute_url()
            url += '/@@thanks_trader_view?uuid=' + uuid
            # url = addTokenToUrl(url)
            # import pdb;pdb.set_trace()
            self.request.response.redirect(url)
        finally:
            # Restore the old security manager
            setSecurityManager(sm)

    @button.buttonAndHandler(_(u'Cancel registration'))
    def handleCancel(self, action):
        data, errors = self.extractData()
        # context is the thesis repo
        contextURL = self.context.absolute_url()
        self.request.response.redirect(contextURL)


class AddView(add.DefaultAddView):
    form = AddForm
