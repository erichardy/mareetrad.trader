# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
from zope.schema import TextLine
# from plone.autoform import directives as form
from collective import dexteritytextindexer
from plone.dexterity.content import Container
# from plone.namedfile import field as namedfile
from plone.supermodel import model
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import implementer

from mareetrad.trader.utils import validateEmail
from mareetrad.trader import _

for_trader_txt = u"""
<h2>Vous venez de vous inscrire pour la Marée Trad 2018 !</h2>
<p>Vous avez saisi les éléments ci-dessous :</p>
<p>_trader_description_</p>
<p>Vous serez averti de la suite des événements à partir du 20
mai 2018</p>
<p> </p>
"""


class IMareetrad(model.Schema):
    """ Marker interfce and Dexterity Python Schema for Mareetrad
    """

    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
        title=_(u'email adress'),
        description=_(u'required to inform you'),
        default=u'Marée Trad 2018',
        required=True
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

    # directives.widget(level=RadioFieldWidget)
    # level = schema.Choice(
    #     title=_(u'Sponsoring Level'),
    #     vocabulary=LevelVocabulary,
    #     required=True
    # )

    # text = RichText(
    #     title=_(u'Text'),
    #     required=False
    # )

    # url = schema.URI(
    #     title=_(u'Link'),
    #     required=False
    # )

    # fieldset('Images', fields=['logo', 'advertisement'])
    # logo = namedfile.NamedBlobImage(
    #     title=_(u'Logo'),
    #     required=False,
    # )

    # advertisement = namedfile.NamedBlobImage(
    #     title=_(u'Advertisement (Gold-sponsors and above)'),
    #     required=False,
    # )

    # directives.read_permission(notes='cmf.ManagePortal')
    # directives.write_permission(notes='cmf.ManagePortal')
    # notes = RichText(
    #     title=_(u'Secret Notes (only for site-admins)'),
    #     required=False
    # )


@implementer(IMareetrad)
class Mareetrad(Container):
    """
    """
