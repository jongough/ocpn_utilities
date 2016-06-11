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
from classes.saverestorefilesdef import SaveRestoreFilesDef
from classes.language import Language

###########################################################################
## Class SaveRestoreFilesImpl
###########################################################################

class SaveRestoreFilesImpl ( SaveRestoreFilesDef ):
	
	def __init__(self, parent, title):
		SaveRestoreFilesDef.__init__(self, parent)
#		conf = Conf()
#		Language(conf.get('GENERAL','lang'))
		
		self.m_buttonSave.Disable()
		self.m_buttonRestore.Disable()
		self.dirSelected = False
		self.SaveSetSelected = False
		
		self.Layout()
		self.GetSizer().Fit(self)
		self.Centre( wx.CENTER_ON_SCREEN )
		self.Show(True)
	
	def __del__( self ):
		pass
#	
# Event section
#
	def OnCheckBoxAll( self, event ):
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

	def OnCheckBoxOCPNConf( self, event ):
		self.SetIsChecked()
		self.SetButtons()
		
		SaveRestoreFilesDef.OnCheckBoxOCPNConf(self, event)

	def OnCheckBoxOPConf( self, event ):
		self.SetIsChecked()
		self.SetButtons()
		
		SaveRestoreFilesDef.OnCheckBoxOPConf(self, event)

	def OnCheckBoxOCPNData( self, event ):
		self.SetIsChecked()
		self.SetButtons()
		
		SaveRestoreFilesDef.OnCheckBoxOCPNData(self, event)

	def OnCheckBoxPluginData( self, event ):
		self.SetIsChecked()
		self.SetButtons()
		
		SaveRestoreFilesDef.OnCheckBoxPluginData(self, event)
	
	def OnDirChanged( self, event ):
		self.Layout()
		self.GetSizer().Fit(self)
		
		if self.m_dirPickerFileDir.GetPath() != "<none>" :
			self.dirSelected = True
			self.SetButtons()
			
		SaveRestoreFilesDef.OnDirChanged(self, event)
		
	def OnDirLeftUp( self, event ):
		testdir = self.m_dirPickerFileDir.GetPath()	
		print('OnDirLeftUp: ' + testdir)
		if self.m_dirPickerFileDir.GetPath() != "<none>" :
			print(testdir)
			self.dirSelected = True
			self.SetButtons()
			
		SaveRestoreFilesDef.OnDirLeftUp(self, event)

	def OnKillFocus(self, event):
		print('kill focus: ' + self.m_dirPickerFileDir.GetPath())
		
	def OnSaveClick( self, event ):
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
					
		if opencpn_found == True:
			wx.MessageBox('OpenCPN is running. Please stop it before saving a copy of the configuration file', 'Info', wx.OK | wx.ICON_INFORMATION)
			return
		currTimeDate = datetime.today().strftime("%Y%m%d-%H%M%S")
		self.dest = self.m_dirPickerFileDir.GetPath() + '/' + currTimeDate
		if not os.path.exists(self.dest):
			os.makedirs(self.dest)
		self.errorMsg = ''
		if self.m_checkBoxAll.IsChecked():
			self.saveOCPNConf()
			self.saveOPConf()
			self.saveOCPNData()
			self.savePluginData()
		else:
			if self.m_checkBoxOCPNConfig.IsChecked():
				self.saveOCPNConf()
			if self.m_checkBoxOpenPlotterConfig.IsChecked():
				self.saveOPConf()
			if self.m_checkBoxOCPNData.IsChecked():
				self.saveOCPNData()
			if self.m_checkBoxPluginData.IsChecked():
				self.savePluginData()
			
		if len(self.errorMsg) != 0 :
			wx.MessageBox('Errors saving\n' + self.errorMsg, 'Info', wx.OK | wx.ICON_INFORMATION)
		
		self.m_staticTextMessage.SetLabel('Save process completed')
		#wx.MessageBox('Save process completed.\n Files stored in directory:\n' + self.dest, 'Info', wx.OK | wx.ICON_INFORMATION )
		
		SaveRestoreFilesDef.OnSaveClick(self, event)
		
	def OnRestoreClick( self, event ):
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
					
		if opencpn_found == True:
			wx.MessageBox('OpenCPN is running. Please stop it before restring a copy of the configuration file', 'Info', wx.OK | wx.ICON_INFORMATION)
			opencpn_found = False
			return
		if openplotter_found == True:
			wx.MessageBox('OpenPlotter is running. Please stop it before restring a copy of the configuration file', 'Info', wx.OK | wx.ICON_INFORMATION)
			openplotter_found = False
			return

		self.source = self.m_dirPickerFileDir.GetPath()
		if not os.path.exists(self.source):
			wx.MessageBox('The source directory ' + self.source + ' does not exist.', 'Info', wx.OK | wx.ICON_ERROR)
			return
		
		self.errorMsg = ''
		if self.m_checkBoxAll.IsChecked():
			self.restoreOCPNConf()
			self.restoreOPConf()
			self.restoreOCPNData()
			self.restorePluginData()
		else:
			if self.m_checkBoxOCPNConfig.IsChecked():
				self.restoreOCPNConf()
			if self.m_checkBoxOpenPlotterConfig.IsChecked():
				self.restoreOPConf()
			if self.m_checkBoxOCPNData.IsChecked():
				self.restoreOCPNData()
			if self.m_checkBoxPluginData.IsChecked():
				self.restorePluginData()
			
		if len(self.errorMsg) != 0 :
			wx.MessageBox('Errors restoring\n' + self.errorMsg, 'Info', wx.OK | wx.ICON_INFORMATION)

		self.m_staticTextMessage.SetLabel('Restore process completed')
		#wx.MessageBox('Restore process completed.', 'Info', wx.OK | wx.ICON_INFORMATION )

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
			shutil.copy2(paths.home +'/.opencpn/opencpn.conf', self.dest)
		else:
			self.errorMsg += 'OpenCPN conf file not found here: ' + paths.home + '/.opencpn/opencpn.conf\n'
	
	def saveOPConf(self):
		if os.path.exists(paths.home + '/.config/openplotter.conf'):
			shutil.copy2(paths.home +'/.config/openplotter.conf', self.dest)
		else:
			self.errorMsg += 'Open Plotter conf file not found here: ' + paths.home + '/.config/openplotter.conf\n'
			
		
	def saveOCPNData(self):
		names = os.listdir(paths.home + '/.opencpn')
		for name in names:
			if 'navobj.xml' in name or 'opencpn.log' in name:
				try:
					if not os.path.isdir(paths.home + '/.opencpn/' + name) :
						shutil.copy2(paths.home + '/.opencpn/' + name, self.dest)
				except (IOError, os.error) as why:
					errors.append((srcname, dstname, str(why)))
				except Error as err:
					errors.extend(err.args[0])				
					
	def savePluginData(self):
		shutil.copytree(paths.home + '/.opencpn/plugins', self.dest + '/plugins', )
		
	def restoreOCPNConf(self):
		if os.path.exists(self.source + '/opencpn.conf'):
			shutil.copy2(self.source + '/opencpn.conf', paths.home +'/.opencpn')
		else:
			self.errorMsg += 'OpenCPN conf file not found here: ' + self.source + '/opencpn.conf\n'
	
	def restoreOPConf(self):
		if os.path.exists(self.soource + '/openplotter.conf'):
			shutil.copy2(self.source + '/openplotter.conf', paths.home +'/.config')
		else:
			self.errorMsg += 'Open Plotter conf file not found here: ' + self.source + '/openplotter.conf\n'
			
		
	def restoreOCPNData(self):
		names = os.listdir(self.source)
		for name in names:
			if 'navobj.xml' in name or 'opencpn.log' in name:
				try:
					if not os.path.isdir(self.source + name) :
						shutil.copy2(self.source + name, paths.home + '/.opencpn/')
				except (IOError, os.error) as why:
					errors.append((srcname, dstname, str(why)))
				except Error as err:
					errors.extend(err.args[0])				
					
	def restorePluginData(self):
		shutil.copytree(self.source + '/plugins', paths.home + '/.opencpn/plugins')
		
app = wx.App(False)

paths = Paths()
bitmap = wx.Bitmap(paths.currentpath + '/star.jpg', wx.BITMAP_TYPE_JPEG)
splash = wx.SplashScreen(bitmap, wx.SPLASH_CENTRE_ON_SCREEN|wx.SPLASH_TIMEOUT, 500, None, style=wx.SIMPLE_BORDER|wx.STAY_ON_TOP)
wx.Yield()
frame = SaveRestoreFilesImpl(None, 'Eclipse Easy-nav Backup/Restore')
app.MainLoop()
		

