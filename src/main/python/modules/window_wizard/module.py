# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inject

from lib.plugin import Loader

from .actions import ModuleActions


class Loader(Loader):
    actions = ModuleActions()

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_provider('wizard', self._widget)

    @inject.params(kernel='kernel', config='config')
    def _widget(self, kernel=None, config=None):
        if len(config.get('storage.location')) and len(config.get('cryptography.password')): return None

        from .gui.dashboard import WizardDashboardScrollArea

        widget = WizardDashboardScrollArea()

        from .gui.wizard.storage import WizardSettingsStorage

        wizard_storage = WizardSettingsStorage()
        wizard_storage.location.connect(self.actions.onActionWizardLocation)
        widget.addWidget(wizard_storage)

        from .gui.wizard.cryptography import WizardSettingsCryptography
        wizard_cryptography = WizardSettingsCryptography()
        wizard_cryptography.password.connect(self.actions.onActionWizardPassword)
        widget.addWidget(wizard_cryptography)

        from .gui.wizard.start import WizardSettingsStart
        wizard_start = WizardSettingsStart()
        wizard_start.start.connect(widget.start.emit)
        widget.addWidget(wizard_start)

        return widget
