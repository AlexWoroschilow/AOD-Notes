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
import functools

from .actions import ModuleActions
from .gui.settings.storage import WidgetSettingsStorage


def service_settings_decorator(func):
    @inject.params(factory='settings_factory')
    def wrapper(this, options, args, factory):
        def settings(actions=None):
            widget = WidgetSettingsStorage()
            if actions is not None and hasattr(actions, 'onActionLocation'):
                widget.locationAction.connect(actions.onActionLocation)
            return widget

        factory.addWidget(functools.partial(
            settings, actions=ModuleActions()
        ))

        return func(this, options, args)

    return wrapper
