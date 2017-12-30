# -*- coding: utf-8 -*-

from plone import api
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.dexterity.browser import add

from plone.supermodel import model
from Products.Five import BrowserView
from z3c.form import button
from zope import schema
from z3c.form.interfaces import IEditForm
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

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

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
        description=_(u'your family name hidden'),
        default=u'Nomm',
        )
    dexteritytextindexer.searchable('firstname')
    firstname = schema.TextLine(
        title=_(u'trader firstame'),
        description=_(u'your first name hidden'),
        default=u'Prééénomm',
        )
    dexteritytextindexer.searchable('pseudo')
    pseudo = schema.TextLine(
        title=_(u'trader pseudo'),
        description=_(u'pseudo'),
        default=u'pseudo',
        )
    dexteritytextindexer.searchable('town')
    town = schema.TextLine(
        title=_(u'the town where you live'),
        description=_(u''),
        default=u'Brest',
        required=False,
        )
    age = schema.Int(
        title=_(u'your age'),
        description=_(u'age hidden'),
        min=1,
        max=110,
        default=33,
        )
    mobile = schema.TextLine(
        title=_(u'mobile phone number'),
        description=_(u'required to inform you, hidden'),
        default=u'123123123',
        )
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'email adress'),
        description=_(u'required to inform you, hidden'),
        constraint=validateEmail,
        default=u'aze.qsd@poi.fr'
        )
    instrument = schema.Choice(
        title=_(u'instrument played at the maree trad'),
        description=_(u'if your instrument is not there, choose "Other"'),
        source='trader.instruments',
        default=u'',
        required=True,
        )
    other_instrument = schema.TextLine(
        title=_(u'instrument played if not in the list above'),
        description=_(u'do not enter an instrument name which yet above'),
        required=True,
        )
    form.omitted('register_date')
    form.no_omit(IEditForm, 'register_date',)
    register_date = schema.Datetime(
        title=_(u'registring date'),
        required=False,
        # defaultFactory=registerDate
        )


@implementer(ITrader)
class Trader(Item):
    """
    """


class View(BrowserView):
    title = _(u'view')

    def listRawFields(self):
        context = self.context
        # out = OrderedDict()
        out = []
        fields = schema.getFieldsInOrder(ITrader)
        for name, field in fields:
            out.append((name, getattr(context, name, None)))
        return out


class AddForm(add.DefaultAddForm):
    portal_type = 'trader'
    ignoreContext = True
    label = _(u'register a new trader !')
    template = ViewPageTemplateFile('trader_add_view.pt')

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
