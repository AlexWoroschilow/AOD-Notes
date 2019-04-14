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
import os
import inject


class ModuleActions(object):

    @inject.params(config='config', kernel='kernel')
    def onActionStorageLocationChange(self, event, config, widget, kernel):

        from PyQt5 import QtWidgets
        destination = str(
            QtWidgets.QFileDialog.getExistingDirectory(widget, "Select Directory", os.path.expanduser('~')))
        if destination is not None and len(destination):
            config.set('storage.location', destination)
            widget.location.setText(destination)
            kernel.dispatch('config_updated')

    @inject.params(config='config', kernel='kernel')
    def onActionCheckboxToggle(self, status, variable, config, kernel):
        config.set(variable, '%s' % status)
        kernel.dispatch('config_updated')
