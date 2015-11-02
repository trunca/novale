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
<screen name="SFsearchupgrade" position="center,160" size="750,370" title="sf_title" >
    <ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/share/enigma2/skin_default/iconos/red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/share/enigma2/skin_default/iconos/green.png" alphatest="blend" />
        
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
<screen name="SFsearchupgrade" position="center,160" size="750,370" title="sf_title" >
        <widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
		<widget source="key_green" render="Label" position="190,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<ePixmap position="190,358" zPosition="1" size="170,2" pixmap="/usr/share/enigma2/skin_default/iconos/green.png" alphatest="blend" />
	<ePixmap position="360,358" zPosition="1" size="170,2" pixmap="/usr/share/enigma2/skin_default/iconos/yellow.png" transparent="1" alphatest="on" />
	<widget source="key_yellow" render="Label" position="360,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<widget source="key_blue" render="Label" position="530,328" zPosition="2" size="170,30" valign="center" halign="center" font="Regular;22" transparent="1" />
	<ePixmap position="530,358" zPosition="1" size="170,2" pixmap="/usr/share/enigma2/skin_default/iconos/blue.png" transparent="1" alphatest="on" />
    <widget source="menu" render="Listbox" position="20,10" size="710,300" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (51, 40), png = 2), # index 4 is the pixmap
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
