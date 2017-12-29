# -*- coding: utf-8 -*-

import re
from zope.interface import Invalid

import logging
from mareetrad.trader import _

logger = logging.getLogger('mareetrad.trader:trader')
checkEmail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}').match


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u'Invalid adress email'))
    return True
