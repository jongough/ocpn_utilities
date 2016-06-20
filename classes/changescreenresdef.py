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
## Class ChangeScreenResDef
###########################################################################

class ChangeScreenResDef ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Change Screen resolution", pos = wx.DefaultPosition, size = wx.Size( 352,247 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		m_fgSizerMain = wx.FlexGridSizer( 0, 1, 0, 0 )
		m_fgSizerMain.AddGrowableCol( 0 )
		m_fgSizerMain.SetFlexibleDirection( wx.BOTH )
		m_fgSizerMain.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer6 = wx.FlexGridSizer( 0, 2, 0, 0 )
		fgSizer6.SetFlexibleDirection( wx.BOTH )
		fgSizer6.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticTextScreenSize = wx.StaticText( self, wx.ID_ANY, u"Width x Height", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextScreenSize.Wrap( -1 )
		fgSizer6.Add( self.m_staticTextScreenSize, 0, wx.ALL, 5 )
		
		m_listBoxScreenSizeChoices = []
		self.m_listBoxScreenSize = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, m_listBoxScreenSizeChoices, wx.LB_SINGLE )
		fgSizer6.Add( self.m_listBoxScreenSize, 0, wx.ALL, 5 )
		
		self.m_staticTextScreenWidth = wx.StaticText( self, wx.ID_ANY, u"Screen Width", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextScreenWidth.Wrap( -1 )
		fgSizer6.Add( self.m_staticTextScreenWidth, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_textCtrlScreenWidth = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.m_textCtrlScreenWidth, 0, wx.ALL, 5 )
		
		self.m_staticTextScreeHeight = wx.StaticText( self, wx.ID_ANY, u"Screen Height", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextScreeHeight.Wrap( -1 )
		fgSizer6.Add( self.m_staticTextScreeHeight, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_textCtrlScreenHeight = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer6.Add( self.m_textCtrlScreenHeight, 0, wx.ALL, 5 )
		
		
		m_fgSizerMain.Add( fgSizer6, 1, wx.EXPAND, 5 )
		
		fgSizer3 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer3.SetFlexibleDirection( wx.BOTH )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_buttonApply = wx.Button( self, wx.ID_ANY, u"&Apply", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonApply, 0, wx.ALL, 5 )
		
		self.m_buttonDefault = wx.Button( self, wx.ID_ANY, u"Default", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonDefault, 0, wx.ALL, 5 )
		
		self.m_buttonCancel = wx.Button( self, wx.ID_ANY, u"&Cancel", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer3.Add( self.m_buttonCancel, 0, wx.ALL, 5 )
		
		
		m_fgSizerMain.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		m_fgSizerMessage = wx.FlexGridSizer( 0, 1, 0, 0 )
		m_fgSizerMessage.AddGrowableCol( 0 )
		m_fgSizerMessage.SetFlexibleDirection( wx.BOTH )
		m_fgSizerMessage.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticTextMessage = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticTextMessage.Wrap( -1 )
		m_fgSizerMessage.Add( self.m_staticTextMessage, 0, wx.ALL, 5 )
		
		self.m_staticText7 = wx.StaticText( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText7.Wrap( -1 )
		m_fgSizerMessage.Add( self.m_staticText7, 0, wx.ALL, 5 )
		
		
		m_fgSizerMain.Add( m_fgSizerMessage, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( m_fgSizerMain )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.m_listBoxScreenSize.Bind( wx.EVT_LISTBOX, self.OnListBoxSelect )
		self.m_textCtrlScreenWidth.Bind( wx.EVT_KILL_FOCUS, self.OnKillFocus )
		self.m_textCtrlScreenHeight.Bind( wx.EVT_KILL_FOCUS, self.OnKillFocus )
		self.m_buttonApply.Bind( wx.EVT_BUTTON, self.OnApplyClick )
		self.m_buttonDefault.Bind( wx.EVT_BUTTON, self.OnDefaultClick )
		self.m_buttonCancel.Bind( wx.EVT_BUTTON, self.OnCancelClick )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def OnListBoxSelect( self, event ):
		event.Skip()
	
	def OnKillFocus( self, event ):
		event.Skip()
	
	
	def OnApplyClick( self, event ):
		event.Skip()
	
	def OnDefaultClick( self, event ):
		event.Skip()
	
	def OnCancelClick( self, event ):
		event.Skip()
	

