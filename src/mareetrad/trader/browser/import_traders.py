# -*- coding: utf-8 -*-

from datetime import datetime
from plone import api
from plone.namedfile.field import NamedBlobFile
from z3c.form import button
import logging
from zope import interface
from z3c.form import form
from z3c.form import field

from mareetrad.trader import _

logger = logging.getLogger('mareetrad.trader:CSV')


class IImportCSV(interface.Interface):
    csv = NamedBlobFile(title=u'CSV des traders a importer')


class importTraders(form.Form):
    fields = field.Fields(IImportCSV)
    ignoreContext = True

    label = _(u'import csv file...')
    description = _(u'This will create traders')

    def processCSV(self, csv):
        lines = csv.split('\n')
        for line in lines:
            # logger.info(line)
            # logger.info('-----------')
            attrs = line.split('|')
            try:
                trader = api.content.create(
                    container=self.context,
                    type='trader',
                    pseudo=attrs[0],
                    town=attrs[1],
                    name=attrs[2],
                    firstname=attrs[3],
                    age=eval(attrs[4]),
                    mobile=attrs[5],
                    title=attrs[6],
                    register_date=datetime.strptime(attrs[7], '%Y/%M/%d'),
                    instrument=eval(attrs[8])[0],
                    other_instrument=attrs[9]
                    )
                instrument = eval(attrs[8])[0].lower()
                if instrument == 'autre':
                    trader.instrument = instrument
                trader.register_date = datetime.strptime(attrs[7], '%Y/%M/%d')
                trader.reindexObject()
            except Exception:
                logger.info(line)

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        csv = data['csv'].data
        self.processCSV(csv)
        self.status = 'Thank you very much!'
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u'Cancel')
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
