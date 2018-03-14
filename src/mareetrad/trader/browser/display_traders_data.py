# -*- coding: utf-8 -*-

from zope.publisher.browser import BrowserView
import logging


logger = logging.getLogger('mareetrad.trader:Thanks: ')


class displayTradersData(BrowserView):
    """
    display all informations about traders, including private data
    like email adress or phone
    """
    pass
