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


def service_config_decorator(func):
    def wrapper(this, store, action):
        location = action.get('location')
        if location is None or not len(location):
            return func(this, store, action)

        container = inject.get_injector_or_die()
        config = container.get_instance('config')

        config.set('storage.location', location)
        config.set('storage.selected.document', '')
        config.set('storage.selected.group', '')

        return func(this, store, action)

    return wrapper


def service_search_decorator(func):
    def wrapper(this, store, action):
        container = inject.get_injector_or_die()
        search = container.get_instance('search')
        print(search)

        return func(this, store, action)

    return wrapper
