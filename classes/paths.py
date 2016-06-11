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

import os, sys

class Paths:

    def __init__(self):

        self.home = os.path.expanduser('~')
        self.pathname = os.path.dirname(sys.argv[0])
        self.currentpath = os.path.abspath(self.pathname)