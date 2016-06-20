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

import os, sys, shutil, subprocess
import wx
import wx.xrc
import psutil
from datetime import datetime
from classes.paths import Paths
from classes.conf import Conf
from classes.changescreenresdef import ChangeScreenResDef
from classes.language import Language


###########################################################################
## Class SaveRestoreFilesImpl
###########################################################################

class ChangeScreenResImpl(ChangeScreenResDef):
    def __init__(self, parent, title):
        ChangeScreenResDef.__init__(self, parent)
        #		conf = Conf()
        #		Language(conf.get('GENERAL','lang'))
        self.errorMsg = ''
        self.SetTitle(title)

        self.Screens = {}
        self.Screens = ['800x600','1024x520','1024x768','1024x600','1152x864','1280x720','1280x800','1280x1024',\
                        '1360x768','1366x768','1440x900','1536x864','1600x1200','1600x900','1680x1050',\
                        '1920x1200','1920x1080','2560x1600','2560x1440','3840x2160']
                        
        for i in range(0,len(self.Screens)):
            self.m_listBoxScreenSize.Append( self.Screens[i] )
        
        self.getBootConf()
        self.m_textCtrlScreenHeight.SetValue(str(self.framebuffer_height))
        self.m_textCtrlScreenHeight.MarkDirty()
        self.m_textCtrlScreenWidth.SetValue(str(self.framebuffer_width))
        self.m_textCtrlScreenWidth.MarkDirty()
        foundSize = False
        currentSize = self.framebuffer_width + 'x' + self.framebuffer_height
        if(currentSize in self.Screens):
            self.m_listBoxScreenSize.SetSelection(self.Screens.index(currentSize))
        else:
            self.m_listBoxScreenSize.Insert(currentSize, 0)
            self.m_listBoxScreenSize.SetSelection(0)
            
        self.Fit()
        #self.Layout()  
        self.Show(True)

    def __del__(self):
        pass

    #
    # Event section
    #
    def OnListBoxSelect( self, event ):
        self.SelectionIndex = self.m_listBoxScreenSize.GetSelection()
        currentSize = self.m_listBoxScreenSize.GetString(self.SelectionIndex)
        currentWidth = currentSize.split('x')[0]
        self.m_textCtrlScreenWidth.SetValue(currentSize.split('x')[0])
        self.m_textCtrlScreenWidth.MarkDirty()
        self.m_textCtrlScreenHeight.SetValue(currentSize.split('x')[1])
        self.m_textCtrlScreenHeight.MarkDirty()
        self.m_staticTextMessage.SetLabel('')
        ChangeScreenResDef.OnListBoxSelect( self, event )

    def OnDefaultClick( self, event ):
        default = self.m_listBoxScreenSize.FindString('1024x768')
        self.m_listBoxScreenSize.SetSelection(default)
        currenSize = self.m_listBoxScreenSize.GetString(default)
        self.SelectionIndex = default
        self.m_textCtrlScreenWidth.SetValue(currenSize.split('x')[0])
        self.m_textCtrlScreenWidth.MarkDirty()
        self.m_textCtrlScreenHeight.SetValue(currenSize.split('x')[1])
        self.m_textCtrlScreenHeight.MarkDirty()
        self.m_staticTextMessage.SetLabel('')
        ChangeScreenResDef.OnDefaultClick(self, event)

    def OnCancelClick( self, event ):
        exit()

    def OnApplyClick(self, event):
        self.saveBootConf()
        if len(self.errorMsg) != 0:
            wx.MessageBox('Errors saving\n' + self.errorMsg, 'Info', wx.OK | wx.ICON_ERROR)
            self.errorMsg = ''
            self.m_staticTextMessage.SetLabel('Save process failed')
        else:
            currentSize = self.m_textCtrlScreenWidth.GetValue() + 'x' + self.m_textCtrlScreenHeight.GetValue()
            if(currentSize not in self.Screens):
                self.m_listBoxScreenSize.Insert(currentSize, 0)
                self.m_listBoxScreenSize.SetSelection(0)
                self.Screens.insert(0, currentSize)
            self.m_staticTextMessage.SetLabel('Screen size applied')
        ans = wx.MessageBox("To change screen size you need to reboot.\nDo you want to reboot now?", "Reboot?", wx.YES_NO)
        if ans == wx.YES:
            self.restart()
        ChangeScreenResDef.OnSaveClick(self,event)

    def OnKillFocus(self, event):
        width = self.m_textCtrlScreenWidth.GetValue()
        height = self.m_textCtrlScreenHeight.GetValue()
        if not width.isdigit():
            self.m_staticTextMessage.SetLabel("Screen width is not a number")
            self.m_textCtrlScreenWidth.SetFocus()
        else:
            if not height.isdigit():
                self.m_staticTextMessage.SetLabel("Screen height is not a number")
                self.m_textCtrlScreenHeight.SetFocus()
            
    #
    # Action section
    #

    def saveBootConf(self):
        if os.path.exists('/boot/config.txt'):
            configFile = '/boot/config.txt'
            newConfigFile = '/boot/config.txt.new'
            newConfFile = open(newConfigFile, 'w')
            foundPlotter = False
            with open(configFile, 'r') as confFile:
                for line in confFile:
                    if '[OPENPLOTTER]' in line:
                        foundPlotter = True
                        newConfFile.write(line)
                        continue
                    if foundPlotter == True and 'framebuffer_width' in line:
                        if line[0] == '#':
                            newConfFile.write(line)
                            continue
                        else:
                            newConfFile.write('framebuffer_width=' + self.m_textCtrlScreenWidth.GetValue() + '\n')
                            foundWidth = True
                            continue
                    if foundPlotter == True and 'framebuffer_height' in line:
                        if line[0] == '#':
                            newConfFile.write(line)
                            continue
                        else:
                            newConfFile.write('framebuffer_height=' + self.m_textCtrlScreenHeight.GetValue() + '\n')
                            foundHeight = True
                            continue
                    newConfFile.write(line)
                    
                confFile.close()
                newConfFile.close()
                os.rename(configFile, configFile + '.old')
                os.rename(newConfigFile, newConfigFile.split('.')[0] + '.' + newConfigFile.split('.')[1])
                currenSize = self.m_textCtrlScreenWidth.GetValue() + 'x' + self.m_textCtrlScreenHeight.GetValue()
                    
        else:
            self.errorMsg += 'Raspberry PI boot config.txt file not found here: /boot/config.txt\n'

    def getBootConf(self):
        #if os.path.exists(paths.home + '/config.txt'):
        if os.path.exists('/boot/config.txt'):
            configFile = '/boot/config.txt'
            foundPlotter = False
            foundWidth = False
            foundHeight = False
            with open(configFile, 'r') as confFile:
                for line in confFile:
                    line = line.rstrip('\n').rstrip('\r')
                    if line == '[OPENPLOTTER]':
                        foundPlotter = True
                        continue
                    if foundPlotter == True and 'framebuffer_width' in line:
                        if line[0] == '#':
                            continue
                        else:
                            self.framebuffer_width = line[line.find('=')+1:]
                            foundWidth = True
                            continue
                    if foundPlotter == True and 'framebuffer_height' in line:
                        if line[0] == '#':
                            continue
                        else:
                            self.framebuffer_height = line[line.find('=')+1:]
                            foundHeight = True
                            continue
                    if foundPlotter and foundWidth and foundHeight:
                        break
                confFile.close()
        else:
            self.errorMsg += 'Raspberry PI boot config.txt file not found here: /boot/config.txt\n'
        if len(self.errorMsg) != 0:
            wx.MessageBox('Errors opening\n' + self.errorMsg, 'Info', wx.OK | wx.CENTRE |wx.ICON_ERROR)
            self.errorMsg = ''
        
    def restart(self):
        command = '/sbin/shutdown -r now'
        import subprocess
        process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

if __name__ == "__main__":
    app = wx.App(False)

    paths = Paths()
    bitmap = wx.Bitmap(paths.currentpath + '/star.jpg', wx.BITMAP_TYPE_JPEG)
    # Not needed at the moment as app starts fast
    # splash = wx.SplashScreen(bitmap, wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 500, None, style=wx.SIMPLE_BORDER|wx.STAY_ON_TOP)
    # wx.Yield()
    frame = ChangeScreenResImpl(None, 'Easy-nav Screen Size')
    ficon = wx.EmptyIcon()
    ficon.CopyFromBitmap(bitmap)
    frame.SetIcon(ficon)
    frame.Raise()

    app.MainLoop()
