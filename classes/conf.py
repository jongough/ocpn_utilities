#!/usr/bin/env python
# -*- coding: utf-8 -*- 

# 
# Project:  OpenCPN
# Purpose:  Raspberry PI OpenCPN config files save/restore
# Author:   Jon Gough
#
# This file is part of OpenCPN Raspberry PI Utilities.
# Copyright (C) 2016 by jongough <https://github.com/jongough/ocpn_utilities>
#
# Openplotter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# any later version.
# Openplotter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Openplotter. If not, see <http://www.gnu.org/licenses/>.
#
# Built with the assistance of Wing IDE ( http://wingware.com )

import ConfigParser
from paths import Paths

class Conf:

    def __init__(self):

        self.paths=Paths()

        self.data_conf = ConfigParser.SafeConfigParser()

        self.read()

    def read(self):
        self.data_conf.read(self.paths.currentpath+'/ocpn_utilities.conf')

    def write(self):
        with open(self.paths.currentpath+'/ocpn_utililties.conf', 'wb') as configfile:
            self.data_conf.write(configfile)

    def get(self,section,item):
        return self.data_conf.get(section,item)

    def set(self,section,item,value):
        self.read()
        self.data_conf.set(section, item, value)
        self.write()