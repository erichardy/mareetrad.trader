# -*- coding: utf-8 -*-

from plone.app.uuid.utils import uuidToObject
from zope.publisher.browser import BrowserView
# from plone.protect import CheckAuthenticator
# from plone.protect import protect
from plone import api
# from zope.interface import alsoProvides
# from plone.protect.interfaces import IDisableCSRFProtection
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import (
    newSecurityManager, setSecurityManager)
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Products.CMFPlone.utils import safe_unicode
from mareetrad.trader.utils import mareeTradMailActivated
import logging


logger = logging.getLogger('mareetrad.trader:Thanks: ')


for_trader_txt = u"""
<h2>Vous venez de vous inscrire pour la Marée Trad 2018</h2>
<p>Vous avez saisi les éléments ci-dessous :</p>
<p>_trader_description_</p>
<p>Vous serez averti de la suite des événements plus tard</p>
<p> </p>
"""


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return 'AnonymousTrader'


class thanksTraderView(BrowserView):

    def getTrader(self):
        # alsoProvides(self.request, IDisableCSRFProtection)
        portal = api.portal.get()
        sm = getSecurityManager()
        self.trader = {}
        # logger.info(self.request.form)
        uuid = self.request.get('uuid')
        tmp_user = UnrestrictedUser(
            sm.getUser().getId(), '', ['Manager'], '')
        tmp_user = tmp_user.__of__(portal.acl_users)
        newSecurityManager(None, tmp_user)
        obj = uuidToObject(uuid)
        # logger.info(obj.getId())
        self.trader = {}
        self.trader['title'] = obj.title
        self.trader['email'] = obj.title
        self.trader['name'] = obj.name
        self.trader['firstname'] = obj.firstname
        self.trader['pseudo'] = obj.pseudo
        self.trader['town'] = obj.town
        self.trader['age'] = str(obj.age)
        self.trader['mobile'] = obj.mobile
        self.trader['reg_date'] = obj.register_date.strftime('%d/%m/%Y %H:%M')
        if obj.instrument == u'autre':
            self.trader['instrument'] = obj.other_instrument
        else:
            self.trader['instrument'] = obj.instrument

        setSecurityManager(sm)
        return self.trader

    def getHTMLContent(self, trader):
        """
        TOTO: prendre le texte à envoyer du dossier parent : mareetrad
        """
        raw = for_trader_txt
        """
        raw = api.portal.get_registry_record(
                'trader_message',
                interface=IMareetradTraderSettings)
        """
        content = u'Nom: ' + trader['name'] + u'<br />'
        content += u'Prénom: ' + trader['firstname'] + u'<br />'
        content += u'email: ' + trader['email'] + u'<br />'
        content += u'Pseudo: ' + trader['pseudo'] + u'<br />'
        content += u'Ville: ' + trader['town'] + u'<br />'
        content += u'Age: ' + trader['age'] + u'<br />'
        content += u'Tel: ' + trader['mobile'] + u'<br />'
        content += u'Instrument: ' + trader['instrument'] + u'<br /><br />'
        content += u'Inscription réalisée le : '
        content += trader['reg_date'] + u'<br />'
        raw = raw.replace(
            u'_trader_description_', content
            )
        return raw

    def sendToTrader(self, htmlContent, recipient):
        if not mareeTradMailActivated(self):
            logger.info('Mails not activated !')
            return
        sender = 'no-reply@maree-trad.net'
        message = MIMEMultipart()
        part = MIMEText(safe_unicode(htmlContent), u'html', _charset='utf-8')
        message.attach(part)
        subject = u'[Marée Trad] Votre inscription'
        try:
            api.portal.send_email(sender,
                                  recipient=recipient,
                                  subject=subject,
                                  body=message)
        except Exception:
            logger.info('Error : mail to ' +
                        recipient + ' Failed !')
