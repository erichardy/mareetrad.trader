# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from plone.autoform import directives as form
from plone.dexterity.content import Item
from plone.namedfile import field as namedfile
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer
from collective import dexteritytextindexer
from mareetrad.trader import _


class ITrader(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Trader
    """
    dexteritytextindexer.searchable('title')
    form.omitted('title')
    title = schema.TextLine(
        title=_(u'ABC Tune name'),
        description=_(u'The name as you know this tune'),
        )
    dexteritytextindexer.searchable('title')
    model.primary('title')
    name = schema.TextLine(
        title=_(u'trader name'),
        description=_(u'your family name'),
        )
    dexteritytextindexer.searchable('firstname')
    firstname = schema.TextLine(
        title=_(u'trader firstame'),
        description=_(u'your first name'),
        )
    dexteritytextindexer.searchable('town')
    town = schema.TextLine(
        title=_(u'the town where you live'),
        description=_(u''),
        )
    age = schema.Int(
        title=_(u'your age'),
        description=_(u'how old are you'),
        min=1,
        max=110,
        )
    mobile = schema.TextLine(
        title=_(u'mobile phone number'),
        description=_(u'required to inform you'),
        )
    email = schema.TextLine(
        title=_(u'email adress'),
        description=_(u'required to inform you'),
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
        )
    form.omitted('register_date')
    register_date = schema.Date(
        title=_(u"registring date"),
        required=False,
        )


@implementer(ITrader)
class Trader(Item):
    """
    """
