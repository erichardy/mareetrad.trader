# -*- coding: utf-8 -*-

# from plone import api
# from zope.component import getUtility
# from plone.i18n.normalizer.interfaces import INormalizer


class setTraderId():

    def __init__(self, context, event):
        # name = context.name
        # firstname = context.firstname
        # context.title = name + '_' + firstname
        # norm = getUtility(INormalizer)
        # newId = norm.normalize(context.title, locale='fr')
        # import pdb;pdb.set_trace()

        # context.id = newId
        context.reindexObject()
