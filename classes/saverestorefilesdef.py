# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class SaveRestoreFilesDef
###########################################################################

class SaveRestoreFilesDef ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Backup/Restore", pos = wx.DefaultPosition, size = wx.Size( 352,305 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.AddGrowableCol( 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticTextSaveRestoreDir = wx.StaticText( self, wx.ID_ANY, u"Save/Restore Directory", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextSaveRestoreDir.Wrap( -1 )
		fgSizer2.Add( self.m_staticTextSaveRestoreDir, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_dirPickerFileDir = wx.DirPickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a folder", wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST|wx.DIRP_USE_TEXTCTRL )
		fgSizer2.Add( self.m_dirPickerFileDir, 1, wx.ALL|wx.EXPAND, 5 )
		
		fgSizer4 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer4.SetFlexibleDirection( wx.BOTH )
		fgSizer4.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_checkBoxAll = wx.CheckBox( self, wx.ID_ANY, u"All", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		fgSizer4.Add( self.m_checkBoxAll, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		self.m_checkBoxOCPNConfig = wx.CheckBox( self, wx.ID_ANY, u"OpenCPN Config", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		fgSizer4.Add( self.m_checkBoxOCPNConfig, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		fgSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_checkBoxOpenPlotterConfig = wx.CheckBox( self, wx.ID_ANY, u"Open Plotter Config", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		fgSizer4.Add( self.m_checkBoxOpenPlotterConfig, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		fgSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_checkBoxOCPNData = wx.CheckBox( self, wx.ID_ANY, u"OCPN Data", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		fgSizer4.Add( self.m_checkBoxOCPNData, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		fgSizer4.AddSpacer( ( 0, 0), 1, wx.EXPAND, 5 )
		
		self.m_checkBoxPluginData = wx.CheckBox( self, wx.ID_ANY, u"Plugin Data", wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
		fgSizer4.Add( self.m_checkBoxPluginData, 0, wx.ALIGN_RIGHT|wx.ALL, 5 )
		
		
		fgSizer2.Add( fgSizer4, 1, wx.EXPAND, 5 )
		
		
		fgSizer1.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonSave = wx.Button( self, wx.ID_ANY, u"&Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonSave.Enable( False )
		
		fgSizer3.Add( self.m_buttonSave, 0, wx.ALL, 5 )
		
		self.m_buttonRestore = wx.Button( self, wx.ID_ANY, u"Restore", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_buttonRestore.Enable( False )
		
		fgSizer3.Add( self.m_buttonRestore, 0, wx.ALL, 5 )
		
		self.m_buttonCancel = wx.Button( self, wx.ID_ANY, u"&Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonCancel, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		m_fgSizerMessage = wx.FlexGridSizer( 0, 1, 0, 0 )
		m_fgSizerMessage.AddGrowableCol( 0 )
		m_fgSizerMessage.SetFlexibleDirection( wx.BOTH )
		m_fgSizerMessage.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticTextMessage = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_LEFT )
		self.m_staticTextMessage.Wrap( -1 )
		m_fgSizerMessage.Add( self.m_staticTextMessage, 0, wx.ALL, 5 )
		
		
		fgSizer1.Add( m_fgSizerMessage, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( fgSizer1 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_dirPickerFileDir.Bind( wx.EVT_DIRPICKER_CHANGED, self.OnDirChanged )
		self.m_checkBoxAll.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxAll )
		self.m_checkBoxOCPNConfig.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxOCPNConf )
		self.m_checkBoxOpenPlotterConfig.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxOPConf )
		self.m_checkBoxOCPNData.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxOCPNData )
		self.m_checkBoxPluginData.Bind( wx.EVT_CHECKBOX, self.OnCheckBoxPluginData )
		self.m_buttonSave.Bind( wx.EVT_BUTTON, self.OnSaveClick )
		self.m_buttonRestore.Bind( wx.EVT_BUTTON, self.OnRestoreClick )
		self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.OnCancelClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnDirChanged( self, event ):
		event.Skip()
	
	def OnCheckBoxAll( self, event ):
		event.Skip()
	
	def OnCheckBoxOCPNConf( self, event ):
		event.Skip()
	
	def OnCheckBoxOPConf( self, event ):
		event.Skip()
	
	def OnCheckBoxOCPNData( self, event ):
		event.Skip()
	
	def OnCheckBoxPluginData( self, event ):
		event.Skip()
	
	def OnSaveClick( self, event ):
		event.Skip()
	
	def OnRestoreClick( self, event ):
		event.Skip()
	
	def OnCancelClick( self, event ):
		event.Skip()
	

