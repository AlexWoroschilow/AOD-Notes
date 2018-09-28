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


class ModuleActions(object):

    @inject.params(kernel='kernel', factory='settings_factory', logger='logger')
    def onActionSettings(self, event=None, factory=None, kernel=None, logger=None):
        logger.debug('[search] settings event')
        kernel.dispatch('window.tab', (factory.widget, 'Settings'))

    @inject.params(config='config', kernel='kernel')
    def onActionToggle(self, status, variable, config, kernel):
        config.set(variable, '%s' % status)
        kernel.dispatch('config_updated')
