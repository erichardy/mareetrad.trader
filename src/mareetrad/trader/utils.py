# -*- coding: utf-8 -*-

from zope.interface import Invalid
# import logging
import re
from mareetrad.trader import _

checkEmail = re.compile(
    r'[a-zA-Z0-9._%-]+@([a-zA-Z0-9-]+\.)*[a-zA-Z]{2,4}').match


def validateEmail(value):
    if not checkEmail(value):
        raise Invalid(_(u'Invalid adress email'))
    return True
