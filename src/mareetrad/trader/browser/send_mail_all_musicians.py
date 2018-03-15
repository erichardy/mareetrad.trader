# -*- coding: utf-8 -*-

from zope.publisher.browser import BrowserView
from plone import api
from plone.app.uuid.utils import uuidToObject
import logging


logger = logging.getLogger('mareetrad.trader:mail to ALL ')


class sendMailAllMusicians(BrowserView):

    def getMusiciansFolders(self):
        portal = api.portal.get()
        folders = api.content.find(
            context=portal,
            portal_type='mareetraders',
            )
        return [(f.getObject(), api.content.get_uuid(obj=f.getObject()))
                for f in folders]

    def getMusicians(self, foldersUUIDs):
        if isinstance(foldersUUIDs, str):
            f = [uuidToObject(foldersUUIDs)]
        else:
            f = [uuidToObject(folder) for folder in foldersUUIDs]
        emails = []
        for mareetraders in f:
            logger.info(mareetraders)
            traders = api.content.find(
                context=mareetraders,
                portal_type='trader',
                )
            for t in traders:
                email = t.getObject().title
                if email not in emails:
                    emails.append(email)
        return emails
