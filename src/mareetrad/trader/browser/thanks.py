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


# @protect(CheckAuthenticator)
# def __init__(self, context, request, REQUEST=None):
