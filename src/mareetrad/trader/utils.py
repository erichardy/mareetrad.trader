# -*- coding: utf-8 -*-

from plone import api
from zope.interface import Invalid
from zope.publisher.browser import BrowserView
import logging
import re
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
# from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import (
    newSecurityManager, setSecurityManager)
from Products.CMFPlone.utils import safe_unicode
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from mareetrad.trader import _

logger = logging.getLogger('mareetrad:dataset')
checkEmail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}').match


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u'Invalid adress email'))
    return True


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return 'AnonymousTrader'


def setUnsecure(sm):
    portal = api.portal.get()
    tmp_user = UnrestrictedUser(
        sm.getUser().getId(), '', ['Manager'], '')
    tmp_user = tmp_user.__of__(portal.acl_users)
    newSecurityManager(None, tmp_user)


def setSecure(sm):
    setSecurityManager(sm)


def sorted_by_date(trader1, trader2):
    """
    Pour tri, les dates les plus récentes en dernier
    """
    d1 = trader1.register_date
    d2 = trader2.register_date
    if d1 > d2:
        return 1
    if d1 < d2:
        return -1
    return 0


def mareeTradMailActivated(context):
    try:
        type_ok = context.portal_type in ['mareetrad', 'trader']
        if not type_ok:
            return False
    except Exception:
        return False
    if context.portal_type == 'trader':
        context = context.aq_parent
    return context.mails_activated


html_head = u'<!doctype html><html><body>'
html_trail = u'</body></html>'


def remove_html_markup(s):
    tag = False
    quote = False
    out = ''
    for c in s:
        if c == '<' and not quote:
            tag = True
        elif c == '>' and not quote:
            tag = False
        elif (c == '"' or c == "'") and tag:
            quote = not quote
        elif not tag:
            out = out + c
    return out


def mailMultipart(raw):
    """
    Crée un message MIMEMultipart à partir d'un texte contenant du HTML.
    Voir candidate_events.py et thesis_events.py
    :param raw: du texte qui contient du html
    :type raw: string
    :returns: un MuiltiPart message que l'on peut envoyer aver
        api.portal.send_email(..., body= message)
    """
    message = MIMEMultipart('alternative')

    raw_text = remove_html_markup(raw)
    part = MIMEText(safe_unicode(raw_text), u'plain', _charset='utf-8')
    message.attach(part)

    raw_html = html_head + raw + html_trail
    part = MIMEText(safe_unicode(raw_html), u'html', _charset='utf-8')
    message.attach(part)

    return message


def publish(obj):
        api.content.transition(obj=obj, transition='publish')


trader1 = {}
trader1['title'] = u'tr1@tr1.tr1'
trader1['pseudo'] = u'tr1 pseudo'
trader1['instrument'] = u'accordéon'
trader1['other_instrument'] = u'Cymballes'
trader1['town'] = u'Brest'
trader1['age'] = 23
trader1['name'] = u'trader1'
trader1['firstname'] = u'fff trader1'
trader1['mobile'] = u'12 23 34 45 56'
trader2 = {}
trader2['title'] = u'tr2@tr2.tr2'
trader2['pseudo'] = u'tr2 pseudo'
trader2['instrument'] = u'tr2 instrument'
trader2['other_instrument'] = u'Cymballes'
trader2['town'] = u'Quimper'
trader2['age'] = 54
trader2['name'] = u'trader2 trader2'
trader2['firstname'] = u'fff trader2'
trader2['mobile'] = u'12 56 54 65 76'

trader3 = {}
trader3['title'] = u'tr3@tr3.tr3'
trader3['pseudo'] = u'tr3 pseudo'
trader3['instrument'] = u'autre'
trader3['other_instrument'] = u'Cymballes'
trader3['town'] = u'Ailleurs'
trader3['age'] = 76
trader3['name'] = u'trader3'
trader3['firstname'] = u'fff trader3'
trader3['mobile'] = u'11 12 22 23 33'

traders = [trader1, trader2, trader3]


class dataSet(BrowserView):

    def __call__(self):
        self.portal = api.portal.get()
        purge = self.request.form.get('purge')
        if purge:
            self.purgeDataSet()
            self.request.response.redirect(self.portal.absolute_url())
            return
        if self.portal.get('maree-trad-2020'):
            logger.info('maree-trad-2020 already exists !!!')
            return
        self.mareetraders = self.createMareeTraders(self.portal)
        publish(self.mareetraders)
        for trader in traders:
            self.createTrader(trader, self.mareetraders)
        self.request.response.redirect(self.mareetraders.absolute_url())

    def createMareeTraders(self, loc):
        return api.content.create(
            container=loc,
            type='mareetraders',
            title=u'Marée Trad 2020',
            mails_activated=False
            )

    def createTrader(self, trader, mareetraders):
        api.content.create(
            container=mareetraders,
            type='trader',
            title=trader['title'],
            pseudo=trader['pseudo'],
            instrument=trader['instrument'],
            other_instrument=trader['other_instrument'],
            town=trader['town'],
            age=trader['age'],
            name=trader['name'],
            firstname=trader['firstname'],
            mobile=trader['mobile'],
            )

    def purgeDataSet(self):
        mt = self.portal.get('maree-trad-2020')
        logger.info(mt)
        api.content.delete(obj=mt)
        try:
            mt = self.portal.get('maree-trad-2020')
            api.content.delete(obj=mt)
        except Exception:
            logger.info('No mareetraders to purge !!!')
            pass
