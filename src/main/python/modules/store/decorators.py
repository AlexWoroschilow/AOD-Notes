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
        container = inject.get_injector_or_die()
        config = container.get_instance('config')

        location = action.get('location')
        if location is not None and len(location):
            config.set('storage.selected.document', '')
            config.set('storage.selected.group', '')
            config.set('storage.location', location)

            return func(this, store, action)

        entity = action.get('entity')
        if entity is not None:
            if entity.__class__.__name__ == 'Group':
                config.set('storage.selected.group', entity.path)
                return func(this, store, action)

            if entity.__class__.__name__ == 'Document':
                config.set('storage.selected.document', entity.path)
                return func(this, store, action)

        return func(this, store, action)

    return wrapper


def service_search_decorator(func):
    def wrapper(this, store, action):
        container = inject.get_injector_or_die()
        search = container.get_instance('search')
        print(search)

        return func(this, store, action)

    return wrapper
