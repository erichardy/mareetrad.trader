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
from mareetrad.trader.interfaces import IMareetradTraderSettings
import logging


logger = logging.getLogger('mareetrad.trader:Thanks: ')


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
        self.trader['email'] = obj.title
        self.trader['name'] = obj.name
        setSecurityManager(sm)
        return self.trader

    def sendToTrader(self):
        sender = api.portal.get_registry_record(
                'mail_sender',
                interface=IMareetradTraderSettings)
        trader = self.getTrader()
        raw = api.portal.get_registry_record(
                'trader_message',
                interface=IMareetradTraderSettings)
        content = u'Nom: ' + trader.name + u'<br />'
        content += u'Prénom: ' + trader.firstname + u'<br />'
        content += u'email: ' + trader.title + u'<br />'
        content += u'Ville: ' + trader.town + u'<br />'
        content += u'Age: ' + str(trader.age) + u'<br />'
        content += u'Tel: ' + trader.mobile + u'<br />'
        if trader.instrument == u'autre':
            try:
                content += u'Intrument: ' + trader.other_instrument + u'<br />'
            except Exception:
                content += u'Intrument: aucun !<br />'
        else:
            content += u'Intrument: ' + trader.instrument + u'<br />'

        recipient = trader.title
        raw = raw.replace(
            u'_trader_description_', content
            )
        message = MIMEMultipart()
        part = MIMEText(safe_unicode(raw), u'html', _charset='utf-8')
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
