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
import glob
import wx
import wx.xrc
import psutil
from distutils.dir_util import copy_tree
from datetime import datetime
from classes.paths import Paths
from classes.conf import Conf
from classes.saverestorefilesdef import SaveRestoreFilesDef
from classes.language import Language


###########################################################################
## Class SaveRestoreFilesImpl
###########################################################################

class SaveRestoreFilesImpl(SaveRestoreFilesDef):
    def __init__(self, parent, title):
        SaveRestoreFilesDef.__init__(self, parent)
        #		conf = Conf()
        #		Language(conf.get('GENERAL','lang'))
        self.SetTitle(title)
        self.m_buttonSave.Disable()
        self.m_buttonRestore.Disable()
        self.dirSelected = False
        self.SaveSetSelected = False
            
        if os.path.exists(paths.home + '/.config/openplotter/openplotter.conf'):
            self.m_bOpenPlotter = True
        else:
            self.m_checkBoxOpenPlotterConfig.Hide()
            self.m_checkBoxOpenPlotterConfig.Disable()
            self.m_bOpenPlotter = False
            
    def __del__(self):
        pass

    #
    # Event section
    #

    def OnCheckBoxAll(self, event):
        if self.m_checkBoxAll.IsChecked():
            self.m_checkBoxOCPNConfig.Disable()
            self.m_checkBoxOCPNData.Disable()
            self.m_checkBoxOpenPlotterConfig.Disable()
            self.m_checkBoxPluginData.Disable()
        else:
            self.m_checkBoxOCPNConfig.Enable()
            self.m_checkBoxOCPNData.Enable()
            self.m_checkBoxOpenPlotterConfig.Enable()
            self.m_checkBoxPluginData.Enable()

        self.SetIsChecked()
        self.SetButtons()

        SaveRestoreFilesDef.OnCheckBoxAll(self, event)

    def OnCheckBoxOCPNConf(self, event):
        self.SetIsChecked()
        self.SetButtons()

        SaveRestoreFilesDef.OnCheckBoxOCPNConf(self, event)

    def OnCheckBoxOPConf(self, event):
        self.SetIsChecked()
        self.SetButtons()

        SaveRestoreFilesDef.OnCheckBoxOPConf(self, event)

    def OnCheckBoxOCPNData(self, event):
        self.SetIsChecked()
        self.SetButtons()

        SaveRestoreFilesDef.OnCheckBoxOCPNData(self, event)

    def OnCheckBoxPluginData(self, event):
        self.SetIsChecked()
        self.SetButtons()

        SaveRestoreFilesDef.OnCheckBoxPluginData(self, event)

    def OnDirChanged(self, event):
        self.Layout()
        self.GetSizer().Fit(self)

        if self.m_dirPickerFileDir.GetPath() != "<none>":
            self.dirSelected = True
            self.SetButtons()
            
        self.m_staticTextMessage.SetLabel('')
        
        SaveRestoreFilesDef.OnDirChanged(self, event)

    def OnDirLeftUp(self, event):
        testdir = self.m_dirPickerFileDir.GetPath()
        if self.m_dirPickerFileDir.GetPath() != "<none>":
            self.dirSelected = True
            self.SetButtons()

        self.m_staticTextMessage.SetLabel('')
            
        SaveRestoreFilesDef.OnDirLeftUp(self, event)

    def OnSaveClick(self, event):
        pythons_psutil = []
        opencpn_found = False
        openplotter_found = False
        for p in psutil.process_iter():
            try:
                if p.name() == 'opencpn':
                    opencpn_found = True
                if p.name() == 'openplotter':
                    openplotter_found = True
            except psutil.Error:
                pass

        if self.m_checkBoxAll.IsChecked or self.m_checkBoxOCPNConfig.IsChecked: 
            if opencpn_found == True:
                wx.MessageBox('OpenCPN is running. Please stop it before saving a copy of the configuration file', 'Info',
                              wx.OK | wx.ICON_INFORMATION)
                return
        if self.m_checkBoxAll.IsChecked or self.m_checkBoxOpenPlotterConfig.IsChecked: 
            if openplotter_found == True:
                wx.MessageBox('OpenPlotter is running. Please stop it before saving a copy of the configuration file', 'Info',
                              wx.OK | wx.ICON_INFORMATION)
                return
        currTimeDate = datetime.today().strftime("%Y%m%d-%H%M%S")
        self.dest = self.m_dirPickerFileDir.GetPath() + '/Easy-nav Backup ' + currTimeDate
        if not os.path.exists(self.dest):
            os.makedirs(self.dest)
        self.errorMsg = ''
        if self.m_checkBoxAll.IsChecked():
            self.saveOCPNConf()
            if self.m_bOpenPlotter:
                self.saveOPConf()
                self.saveSKConf()
                self.saveKPlexConf()
            self.saveOCPNData()
            self.savePluginData()
        else:
            if self.m_checkBoxOCPNConfig.IsChecked():
                self.saveOCPNConf()
            if self.m_checkBoxOpenPlotterConfig.IsChecked():
                self.saveOPConf()
                self.saveKPlexConf()
                self.saveSKConf()
            if self.m_checkBoxOCPNData.IsChecked():
                self.saveOCPNData()
            if self.m_checkBoxPluginData.IsChecked():
                self.savePluginData()

        if len(self.errorMsg) != 0:
            wx.MessageBox('Errors saving\n' + self.errorMsg, 'Info', wx.OK | wx.ICON_INFORMATION)
            self.m_staticTextMessage.SetLabel('Save process completed with errors')
        else:
            self.m_staticTextMessage.SetLabel('Save process completed')

        SaveRestoreFilesDef.OnSaveClick(self, event)

    def OnRestoreClick(self, event):
        pythons_psutil = []
        opencpn_found = False
        openplotter_found = False
        openplotter_serial_found = False
        signalk_found = False
        for p in psutil.process_iter():
            try:
                if p.name() == 'opencpn':
                    opencpn_found = True
                if p.name() == 'openplotter':
                    openplotter_found = True
                if p.name() == 'openplotter-serial':
                    openplotter_serial_found = True
                if p.name() == 'signalk-server':
                    signalk_found = True
                    
            except psutil.Error:
                pass

        if opencpn_found == True:
            wx.MessageBox('OpenCPN is running. Please stop it before restoring a copy of the configuration file', 'Info',
                          wx.OK | wx.ICON_INFORMATION)
            opencpn_found = False
            return
        if openplotter_found == True:
            wx.MessageBox('OpenPlotter is running. Please stop it before restoring a copy of the configuration file',
                          'Info', wx.OK | wx.ICON_INFORMATION)
            openplotter_found = False
            return
        if openplotter_serial_found == True:
            wx.MessageBox('Serial is running. Please stop it before restoring a copy of the configuration file',
                          'Info', wx.OK | wx.ICON_INFORMATION)
            openplotter_serial_found = False
            return
        if signalk_found == True:
            wx.MessageBox('SignalK is running. Please restart it after restoring a copy of the configuration file',
                          'Info', wx.OK | wx.ICON_INFORMATION)
            signalk_found = False

        self.source = self.m_dirPickerFileDir.GetPath()
        if not os.path.exists(self.source):
            wx.MessageBox('The source directory ' + self.source + ' does not exist.', 'Info', wx.OK | wx.ICON_ERROR)
            return

        self.errorMsg = ''
        if self.m_checkBoxAll.IsChecked():
            self.restoreOCPNConf()
            if self.m_bOpenPlotter:
                self.restoreOPConf()
                self.restoreSKConf()
                self.restoreKPlexConf()
            self.restoreOCPNData()
            self.restorePluginData()
        else:
            if self.m_checkBoxOCPNConfig.IsChecked():
                self.restoreOCPNConf()
            if self.m_checkBoxOpenPlotterConfig.IsChecked():
                self.restoreOPConf()
                self.restoreSKConf()
                self.restoreKPlexConf()
            if self.m_checkBoxOCPNData.IsChecked():
                self.restoreOCPNData()
            if self.m_checkBoxPluginData.IsChecked():
                self.restorePluginData()

        if len(self.errorMsg) != 0:
            wx.MessageBox('Errors restoring\n' + self.errorMsg, 'Info', wx.OK | wx.ICON_INFORMATION)
            self.m_staticTextMessage.SetLabel('Restore process completed with errors')
        else:
            self.m_staticTextMessage.SetLabel('Restore process completed')

        SaveRestoreFilesDef.OnRestoreClick(self, event)

    def OnCancelClick(self, event):
        exit()

    def SetButtons(self):
        if self.SaveSetSelected and self.dirSelected:
            self.m_buttonSave.Enable()
            self.m_buttonRestore.Enable()
        else:
            self.m_buttonSave.Disable()
            self.m_buttonRestore.Disable()

    def SetIsChecked(self):
        if self.m_checkBoxAll.IsChecked():
            self.SaveSetSelected = True
        else:
            if self.m_checkBoxOCPNConfig.IsChecked() \
                    or self.m_checkBoxOCPNData.IsChecked() \
                    or self.m_checkBoxOpenPlotterConfig.IsChecked() \
                    or self.m_checkBoxPluginData.IsChecked():
                self.SaveSetSelected = True
            else:
                self.SaveSetSelected = False
            #
            # Action section
            #

    def saveOCPNConf(self):
        if os.path.exists(paths.home + '/.opencpn/opencpn.conf'):
            shutil.copy2(paths.home + '/.opencpn/opencpn.conf', self.dest)
            self.m_staticTextMessage.SetLabel('Saved opencpn.conf')
            wx.Yield()
        else:
            self.errorMsg += 'OpenCPN conf file not found here: ' + paths.home + '/.opencpn/opencpn.conf\n'

    def saveOPConf(self):
        if os.path.exists(paths.home + '/.config/openplotter/openplotter.conf'):
            shutil.copy2(paths.home + '/.config/openplotter/openplotter.conf', self.dest + '/openplotter.conf.config')
            self.m_staticTextMessage.SetLabel('Saved .config/openplotter/openplotter.conf')
            wx.Yield()
        else:
            self.errorMsg += 'Open Plotter .config/openplotter/openplotter.conf file not found here: ' + paths.home + '/.config/openplotter/openplotter.conf\n'

        if os.path.exists(paths.home + '/.openplotter/openplotter.conf'):
            shutil.copy2(paths.home + '/.openplotter/openplotter.conf', self.dest + '/openplotter.conf.openplotter')
            self.m_staticTextMessage.SetLabel('Saved .openplotter/openplotter.conf')
            wx.Yield()
        else:
            self.errorMsg += 'Open Plotter .openplotter/openplotter.conf file not found here: ' + paths.home + '/.openplotter/openplotter.conf\n'

    def saveOCPNData(self):
        names = os.listdir(paths.home + '/.opencpn')
        errors = []
        for name in names:
            if 'navobj.xml' in name or 'opencpn.log' in name:
                try:
                    if not os.path.isdir(paths.home + '/.opencpn/' + name):
                        shutil.copy(paths.home + '/.opencpn/' + name, self.dest)
                        self.m_staticTextMessage.SetLabel('Saved ' + name)
                        wx.Yield()
                except (IOError, os.error) as why:
                    errors.append((srcname, dstname, str(why)))
        if errors:
            raise Exception(errors)

    def savePluginData(self):
        self.m_staticTextMessage.SetLabel('Saving plugin data')
        wx.Yield()
        shutil.copytree(paths.home + '/.opencpn/plugins', self.dest + '/plugins', )
        self.m_staticTextMessage.SetLabel('Saved plugin data')
        wx.Yield()
    
    def saveSKConf(self):
        if os.path.exists(paths.home + '/.signalk/settings.json'):
            json_path = paths.home + '/.signalk/*.json'
            names = glob.glob(paths.home + '/.signalk/*.json')
            dest_path = self.dest + '/.signalk/'
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            errors = []
            for name in names:
                shutil.copy2(name, dest_path)
            if errors:
                raise Exception(errors)
            
            shutil.copy2(paths.home + '/.signalk/signalk-server', dest_path)
            shutil.copytree(paths.home + '/.signalk/plugin-config-data', dest_path + '/plugin-config-data', )
            self.m_staticTextMessage.SetLabel('Saving .signalk settings')
            wx.Yield()
        else:
            self.errorMsg += 'SignalK conf files not found here: ' + paths.home + '/.signalk\n'

    def saveKPlexConf(self):
        if os.path.exists(paths.home + '/.kplex.conf'):
            shutil.copy2(paths.home + '/.kplex.conf', self.dest)
            self.m_staticTextMessage.SetLabel('Saving .kplex.conf')
            wx.Yield()
        else:
            self.errorMsg += 'kplex conf file not found here: ' + paths.home + '/.kplex.conf\n'

    def restoreOCPNConf(self):
        if os.path.exists(self.source + '/opencpn.conf'):
            shutil.copy2(self.source + '/opencpn.conf', paths.home + '/.opencpn')
            self.m_staticTextMessage.SetLabel('Restoring opencpn.conf')
            wx.Yield()
        else:
            self.errorMsg += 'OpenCPN conf file not found here: ' + self.source + '/opencpn.conf\n'

    def restoreOPConf(self):
        if os.path.exists(self.source + '/openplotter.conf.config'):
            shutil.copy2(self.source + '/openplotter.conf.config', paths.home + '/.config/openplotter/openplotter.conf')
            self.m_staticTextMessage.SetLabel('Restoring .config/openplotter/openplotter.conf')
            wx.Yield()
        else:
            self.errorMsg += 'Open Plotter .config/openplotter/openplotter.conf file not found here: ' + self.source + '/openplotter.conf.config\n'

        if os.path.exists(self.source + '/openplotter.conf.openplotter'):
            shutil.copy2(self.source + '/openplotter.conf.openplotter', paths.home + '/.openplotter/openplotter.conf')
            self.m_staticTextMessage.SetLabel('Restoring .openplotter/openplotter.conf')
            wx.Yield()
        else:
            self.errorMsg += 'Open Plotter .openplotter/openplotter.conf file not found here: ' + self.source + '/openplotter.conf.openplotter\n'

    def restoreOCPNData(self):
        names = os.listdir(self.source)
        errors = []
        for name in names:
            if 'navobj.xml' in name or 'opencpn.log' in name:
                try:
                    if not os.path.isdir(self.source + '/' + name):
                        shutil.copy(self.source + '/' + name, paths.home + '/.opencpn/')
                        self.m_staticTextMessage.SetLabel('Restoring ' + name)
                        wx.Yield()
                except (IOError, os.error) as why:
                    errors.append((self.source, paths.home + '/.opencpn/', str(why)))
        if errors:
            raise Exception(errors)

    def restorePluginData(self):
        if os.path.exists(self.source + '/plugins'):
            self.m_staticTextMessage.SetLabel('Restoring plugin data')
            wx.Yield()
            copy_tree(self.source + '/plugins', paths.home + '/.opencpn/plugins')
            self.m_staticTextMessage.SetLabel('Restored plugin data')
            wx.Yield()
        else:
            self.errorMsg += 'Plugin data not found here: ' + self.source + '/plugins\n'
        
    def restoreSKConf(self):
        if os.path.exists(self.source + '/.signalk/settings.json'):
            names = glob.glob(self.source + '/.signalk/*.json')
            dest_path = paths.home + '/.signalk/'
            errors = []
            for name in names:
                shutil.copy2(name, dest_path)
            if errors:
                raise Exception(errors)
            
            shutil.copy2(self.source + '/.signalk/signalk-server', dest_path)
            #shutil.copytree(self.source + '/.signalk/plugin-config-data', dest_path + '/plugin-config-data', dirs_exist_ok=False)
            names = glob.glob(self.source + '/.signalk/plugin-config-data/*')
            errors = []
            for name in names:
                shutil.copy2(name, dest_path + 'plugin-config-data/')
            if errors:
                raise Exception(errors)
            
            self.m_staticTextMessage.SetLabel('Restoring .signalk settings')
            wx.Yield()
        else:
            self.errorMsg += 'SignalK conf files not found here: ' + paths.home + '/.signalk\n'

    def restoreKPlexConf(self):
        if os.path.exists(self.source + '/.kplex.conf'):
            shutil.copy2(self.source + '/.kplex.conf', paths.home)
            self.m_staticTextMessage.SetLabel('Restoring .kplex.conf')
            wx.Yield()
        #else:
         #   self.errorMsg += 'kplex.conf conf file not found here: ' + self.source + '/.kplex.conf\n'
        


if __name__ == "__main__":
    app = wx.App(False)

    paths = Paths()
    bitmap = wx.Bitmap(paths.currentpath + '/star.jpg', wx.BITMAP_TYPE_JPEG)
    # Not needed at the moment as app starts fast
    # splash = wx.SplashScreen(bitmap, wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 500, None, style=wx.SIMPLE_BORDER|wx.STAY_ON_TOP)
    # wx.Yield()
    frame = SaveRestoreFilesImpl(None, 'Easy-nav Backup/Restore')
    ficon = wx.Icon()
    ficon.CopyFromBitmap(bitmap)
    frame.SetIcon(ficon)
    frame.Raise()

    app.MainLoop()
