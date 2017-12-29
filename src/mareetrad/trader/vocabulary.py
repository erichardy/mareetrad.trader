# -*- coding: utf-8 -*-

__docformat__ = 'restructuredtext en'
import logging
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.component import getUtility
from plone import api
from mareetrad.trader.interfaces import IMareetradTraderSettings
from plone.i18n.normalizer.interfaces import INormalizer


logger = logging.getLogger('mareetrad.trader/vocabs')


def make_terms(terms, rawLinesStr):
    normalizer = getUtility(INormalizer)
    rawLines = rawLinesStr.split('\n')
    lines = [l for l in rawLines if l.strip('\r').strip(' ')]
    for line in lines:
        key = normalizer.normalize(line, locale='fr')
        label = line
        terms.append(SimpleVocabulary.createTerm(key, str(key), label))
    return terms


def make_voc(terms, linesstr):
    return SimpleVocabulary(make_terms(terms, linesstr))


def make_voc_with_blank(terms, linesstr):
    terms.append(SimpleVocabulary.createTerm(None, '', u''))
    return SimpleVocabulary(make_terms(terms, linesstr))


class _Instruments(object):
    """Voc. without grok"""
    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        xx_intruments = api.portal.get_registry_record(
                'instruments',
                interface=IMareetradTraderSettings)
        return make_voc_with_blank(terms, xx_intruments)


Instruments = _Instruments()
