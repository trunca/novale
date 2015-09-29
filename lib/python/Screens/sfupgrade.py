# sfteam -- upgrade sfteam
# Copyright (C) www.sfteam.es
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of   
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with GNU gv; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA 02111-1307, USA.
# 
# Author: sfteam
#         
#
# Internet: www.sfteam.es
from Plugins.Plugin import PluginDescriptor
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigSelection, ConfigSubsection, ConfigYesNo,   config, configfile
from Components.ConfigList import ConfigListScreen
from Components.ScrollLabel import ScrollLabel
from Components.Sources.StaticText import StaticText
from Components.ActionMap import ActionMap, NumberActionMap
from Screens.ChoiceBox import ChoiceBox
from Components.config import config, configfile, getConfigListEntry
from Components.ConfigList import ConfigList, ConfigListScreen
from Screens.PluginBrowser import PluginBrowser
from Screens.MessageBox import MessageBox
from Components.MenuList import MenuList
from Components.Sources.List import List
from Tools.LoadPixmap import LoadPixmap
from Plugins.Plugin import PluginDescriptor
from Screens.Console import Console
from Screens.Console import SFConsole
from Screens.Screen import Screen
from Components.Label import Label
from enigma import eTimer, RT_HALIGN_LEFT, eListboxPythonMultiContent, gFont, getDesktop, eSize, ePoint
from Components.Language import language
from Components.Sources.StaticText import StaticText
from Tools.Directories import fileExists
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ
import os
import sys
import gettext

class SFsearchupgrade(Screen):
	skin = """
<screen name="SFsearchupgrade" position="209,48" size="865,623" title="sf_title" flags="wfNoBorder" backgroundColor="transparent">
    <ePixmap pixmap="SF_HD/Bg_EPG_view.png" zPosition="-1" position="0,0" size="865,623" alphatest="on" />
    <ePixmap pixmap="SF_HD/menu/ico_backup.png" position="32,41" size="40,40" alphatest="blend" transparent="1" />
    <widget source="Title" render="Label" position="90,50" size="600,32" font="Semiboldit;32" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1" />
    <ePixmap pixmap="SF_HD/icons/clock.png" position="750,55" zPosition="1" size="20,20" alphatest="blend" />
    <widget source="global.CurrentTime" render="Label" position="770,57" zPosition="1" size="50,20" font="Regular;20" foregroundColor="foreground" backgroundColor="#27d9dee2" halign="right" transparent="1">
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <ePixmap pixmap="SF_HD/border_sf.png" position="125,165" zPosition="-1" size="620,420" transparent="1" alphatest="blend" />
<widget name="key_red" position="86,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget name="key_green" position="278,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<ePixmap pixmap="SF_HD/buttons/red.png" position="45,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/green.png" position="240,98" size="25,25" alphatest="blend" />
        
   </screen>"""
	  
	skin = skin.replace("sf_title", _("SFupgrade - Upgrade Plugins"))  
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("SFsearch upgrade"))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.searchupgrade,
				"red": self.cancel,
				
				
			},-1)
		self['key_red'] = Label(_('Cancel'))
        	self['key_green'] = Label(_('search upgrade'))
		
				
	
	def ok(self):
		self.session.open(SFupgrade)

	def searchupgrade(self):
		self.session.open(SFupgrade)
			

	
	def cancel(self):
		self.close()

#########################################################################################################################################

class SFupgrade(Screen):
	skin = """
<screen name="SFsearchupgrade" position="209,48" size="865,623" title="sf_title" flags="wfNoBorder" backgroundColor="transparent">
    <ePixmap pixmap="SF_HD/Bg_EPG_view.png" zPosition="-1" position="0,0" size="865,623" alphatest="on" />
    <ePixmap pixmap="SF_HD/menu/ico_backup.png" position="32,41" size="40,40" alphatest="blend" transparent="1" />
    <widget source="Title" render="Label" position="90,50" size="600,32" font="Semiboldit;32" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1" />
    <ePixmap pixmap="SF_HD/icons/clock.png" position="750,55" zPosition="1" size="20,20" alphatest="blend" />
    <widget source="global.CurrentTime" render="Label" position="770,57" zPosition="1" size="50,20" font="Regular;20" foregroundColor="foreground" backgroundColor="#27d9dee2" halign="right" transparent="1">
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <ePixmap pixmap="SF_HD/border_sf.png" position="125,165" zPosition="-1" size="620,420" transparent="1" alphatest="blend" />
<widget name="key_red" position="86,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget name="key_green" position="278,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget name="key_blue" position="473,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget name="key_yellow" position="653,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<ePixmap pixmap="SF_HD/buttons/red.png" position="45,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/green.png" position="240,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/blue.png" position="435,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/yellow.png" position="625,98" size="25,25" alphatest="blend" />
    <widget source="menu" render="Listbox" zPosition="1" position="135,180" size="600,450" scrollbarMode="showNever" backgroundColor="#a7a7a7" foregroundColor="#2E2E2E"  transparent="1">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (70, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
			MultiContentEntryText(pos = (80, 29), size = (630, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
			MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
				],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
	</convert>
	</widget>
   
   </screen>"""
	  
	skin = skin.replace("sf_title", _("SFupgrade - Upgrade Plugins"))  
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.setTitle(_("SFupgrade"))
		self.list = []
		self["menu"] = List(self.list)
		self.upgradelist()
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.install,
				"red": self.cancel,
				"blue": self.upgradeall,
				"yellow": self.checkdrivers,
			},-1)
		self.list = [ ]
		self['key_red'] = Label(_('Cancel'))
        	self['key_green'] = Label(_('Install'))
		self['key_blue'] = Label(_('upgrade all'))
		self['key_yellow'] = Label(_('check drivers'))
				
	def upgradelist(self):
		self.list = []
		os.system("opkg update")
		pluginlist = os.popen("opkg list-upgradable | grep enigma2-plugin-extensions-")
                softpng = LoadPixmap(cached=True, path="/usr/share/enigma2/sfpanel/iconmini.png")
		for line in pluginlist.readlines():
			try:
				self.list.append(("%s %s" % (line.split(' - ')[0], line.split(' - ')[1]), line.split(' - ')[-1], softpng))
			except:
				pass
		pluginlist.close()
		self["menu"].setList(self.list)
		
	def ok(self):
		self.setup()
		

	def install(self):
		self.setup()
					

	def setup(self):
		os.system("opkg install %s" % self["menu"].getCurrent()[0])
		self.mbox = self.session.open(MessageBox, _("%s is installed" % self["menu"].getCurrent()[0]), MessageBox.TYPE_INFO, timeout = 4 )

	def upgradeall(self):
		cmd = "/usr/lib/enigma2/python/Screens/SFextra/scripts/upgradeplugin.sh"
		self.session.open(SFConsole,_("Upgrade all Plugins"),[cmd])

	def checkdrivers(self):
		self.session.open(SFConsole,title = _("Check Drivers"), cmdlist = ["sh /usr/lib/enigma2/python/Screens/SFextra/scripts/check_driver.sh"])
		
	def cancel(self):
		self.close()

def main(session, **kwargs):
	session.open(SFsearchupgrade)

def menu(menuid, **kwargs):
	if menuid == "mainmenu":
		return [(_("SFupgrade"), main, _("Install upgrade Plugins"), 48)]
	return []

   	
def Plugins(**kwargs):
    	return [PluginDescriptor(name="SFupgrade", description=_("Install upgrade Plugins"), where = [PluginDescriptor.WHERE_PLUGINMENU], fnc=main, icon="SFupgrade.png"),
		PluginDescriptor(name=_("SFupgrade"), description=_("Install upgrade Plugins"), where = [PluginDescriptor.WHERE_MENU], fnc=menu),
            	PluginDescriptor(name="SFupgrade", description=_("Install upgrade Plugins"), where = PluginDescriptor.WHERE_EXTENSIONSMENU, fnc=main)]
