# -*- coding: utf-8 -*-

from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from mareetrad.trader import _
from mareetrad.trader.interfaces import IMareetradTraderSettings


class IMareetradTraderSettingsForm(RegistryEditForm):
    schema = IMareetradTraderSettings
    label = _(u'Maree-trad trader settings')
    description = _(u'Maree-trad trader Settings Description')

    """
    def updateFields(self):
        super(IIuemAgreementsSettingsForm, self).updateFields()

    def updateWidgets(self):
        super(IIuemAgreementsSettingsForm, self).updateWidgets()
    """


class IMareetradTraderSettingsFormControlPanel(ControlPanelFormWrapper):
    form = IMareetradTraderSettingsForm
