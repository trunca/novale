from enigma import *
from Plugins.SystemPlugins.CrossEPG.crossepglib import *
from Plugins.SystemPlugins.CrossEPG.crossepg_auto import crossepg_auto
from Plugins.SystemPlugins.CrossEPG.crossepg_info import CrossEPG_InfoSF
from Plugins.SystemPlugins.CrossEPG.crossepg_about import CrossEPG_AboutSF
from Plugins.SystemPlugins.CrossEPG.crossepg_providers import CrossEPG_ProvidersSF
from Plugins.SystemPlugins.CrossEPG.crossepg_setup import CrossEPG_SetupSF
from Plugins.SystemPlugins.CrossEPG.crossepg_downloader import CrossEPG_Downloader
from Plugins.SystemPlugins.CrossEPG.crossepg_importer import CrossEPG_Importer
from Plugins.SystemPlugins.CrossEPG.crossepg_converter import CrossEPG_Converter
from Plugins.SystemPlugins.CrossEPG.crossepg_loader import CrossEPG_Loader
from Plugins.SystemPlugins.CrossEPG.crossepg_ordering import CrossEPG_Ordering
from Plugins.SystemPlugins.CrossEPG.crossepg_rytec_update import CrossEPG_Rytec_Update
from Plugins.SystemPlugins.CrossEPG.crossepg_xepgdb_update import CrossEPG_Xepgdb_Update
from Plugins.SystemPlugins.CrossEPG.crossepg_locale import _

from Screens.Screen import Screen
from Screens.MessageBoxSF import MessageBoxSF

from Components.Label import Label
from Components.Button import Button
from Components.MenuList import MenuList
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText
from Components.Harddisk import harddiskmanager
from Components.PluginComponent import plugins
from Components.ActionMap import ActionMap
from Tools.LoadPixmap import LoadPixmap
from Tools.Directories import resolveFilename, SCOPE_PLUGINS
from Plugins.Plugin import PluginDescriptor

from time import *

try:
	from Plugins.SystemPlugins.CrossEPG.version import version
except Exception, e:
	pass

import _enigma

class CrossEPG_SFMenu(Screen):
	def __init__(self, session):
		if (getDesktop(0).size().width() < 800):
			skin = "%s/skins/menu_sd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		else:
			skin = "%s/skins/menu_hd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		f = open(skin, "r")
		self.skin = f.read()
		f.close()
		Screen.__init__(self, session)

		self.config = CrossEPG_Config()
		self.config.load()
		self.patchtype = getEPGPatchType()

		l = []
		l.append(self.buildListEntry(_("Configure CrossEPG"), "configure.png"))
		l.append(self.buildListEntry(_("Epg Providers"), "xmltv.png"))
		l.append(self.buildListEntry(_("Epg Tools"), "conversion.png"))
		l.append(self.buildListEntry(_("Download now"), "download.png"))
		l.append(self.buildListEntry(_("Information"), "about.png"))

		self["list"] = List(l)
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

		self.onFirstExecBegin.append(self.setTitleWithVerion)
		
		if self.config.configured == 0:
			self.onFirstExecBegin.append(self.openSetup)

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image));
		return((pixmap, description))

	def openSetup(self):
		self.session.open(CrossEPG_SetupSF)
			
	def setTitleWithVerion(self):
		try:
			global version
			self.setTitle("CrossEPG Panel")
		except Exception, e:
			self.setTitle("CrossEPG Panel")

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			self.session.open(CrossEPG_SetupSF)
		elif index == 1:
			self.session.open(CrossEPG_SFMenuProviders)
		elif index == 2:
			self.session.open(CrossEPG_SFMenuEpg)
		elif index == 3:
			self.config.load()
			self.config.deleteLog()
			self.downloader()
		elif index == 4:
			self.session.open(CrossEPG_SFMenuInfo)
		
	def quit(self):
		self.close()

	def downloader(self):
		self.config.load()
		self.session.openWithCallback(self.downloadCallback, CrossEPG_Downloader, self.config.providers)

	def downloadCallback(self, ret):
		if ret:
			if self.config.csv_import_enabled == 1:
				self.importer()
			else:
				if self.patchtype != 3:
					self.converter()
				else:
					self.loader()

	def importer(self):
		self.session.openWithCallback(self.importerCallback, CrossEPG_Importer)

	def importerCallback(self, ret):
		if ret:
			if self.patchtype != 3:
				self.converter()
			else:
				self.loader()

	def converter(self):
		self.session.openWithCallback(self.converterCallback, CrossEPG_Converter)

	def converterCallback(self, ret):
		if ret:
			if self.patchtype != -1:
				self.loader()
			else:
				if self.config.download_manual_reboot:
					from Screens.Standby import TryQuitMainloop
					self.session.open(TryQuitMainloop, 3)

	def loader(self):
		self.session.open(CrossEPG_Loader)

class CrossEPG_SFMenuProviders(Screen):
	def __init__(self, session):
		if (getDesktop(0).size().width() < 800):
			skin = "%s/skins/menu_sd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		else:
			skin = "%s/skins/menu_hd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		f = open(skin, "r")
		self.skin = f.read()
		f.close()
		Screen.__init__(self, session)

		self.config = CrossEPG_Config()
		self.config.load()
		self.patchtype = getEPGPatchType()

		l = []
		l.append(self.buildListEntry(_("XMLTV providers"), "xmltv.png"))
		l.append(self.buildListEntry(_("OpenTV providers"), "opentv.png"))
		l.append(self.buildListEntry(_("XEPGDB providers"), "xepgdb.png"))
		l.append(self.buildListEntry(_("Scripts providers"), "scripts.png"))
		l.append(self.buildListEntry(_("MHW2 providers"), "opentv.png"))
		l.append(self.buildListEntry(_("Providers start order"), "reorder.png"))
		l.append(self.buildListEntry(_("Update rytec providers"), "rytec_small.png"))
		l.append(self.buildListEntry(_("Update xepgdb providers"), "xepgdb.png"))

		self["list"] = List(l)
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

		self.onFirstExecBegin.append(self.setTitleWithVerion)
		
		if self.config.configured == 0:
			self.onFirstExecBegin.append(self.openSetup)

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image));
		return((pixmap, description))

	def openSetup(self):
		self.session.open(CrossEPG_SetupSF)
			
	def setTitleWithVerion(self):
		try:
			global version
			self.setTitle("CrossEPG Panel")
		except Exception, e:
			self.setTitle("CrossEPG Panel")

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			self.session.open(CrossEPG_ProvidersSF, "xmltv")
		elif index == 1:
			self.session.open(CrossEPG_ProvidersSF, "opentv")
		elif index == 2:
			self.session.open(CrossEPG_ProvidersSF, "xepgdb")
		elif index == 3:
			self.session.open(CrossEPG_ProvidersSF, "script")
		elif index == 4:
			self.session.open(CrossEPG_ProvidersSF, "mhw2")
		elif index == 5:
			self.session.open(CrossEPG_Ordering)
		elif index == 6:
			self.session.open(CrossEPG_Rytec_Update)
		elif index == 7:
			self.session.open(CrossEPG_Xepgdb_Update)
		
	def quit(self):
		self.close()

	def downloader(self):
		self.config.load()
		self.session.openWithCallback(self.downloadCallback, CrossEPG_Downloader, self.config.providers)

	def downloadCallback(self, ret):
		if ret:
			if self.config.csv_import_enabled == 1:
				self.importer()
			else:
				if self.patchtype != 3:
					self.converter()
				else:
					self.loader()

	def importer(self):
		self.session.openWithCallback(self.importerCallback, CrossEPG_Importer)

	def importerCallback(self, ret):
		if ret:
			if self.patchtype != 3:
				self.converter()
			else:
				self.loader()

	def converter(self):
		self.session.openWithCallback(self.converterCallback, CrossEPG_Converter)

	def converterCallback(self, ret):
		if ret:
			if self.patchtype != -1:
				self.loader()
			else:
				if self.config.download_manual_reboot:
					from Screens.Standby import TryQuitMainloop
					self.session.open(TryQuitMainloop, 3)

	def loader(self):
		self.session.open(CrossEPG_Loader)

class CrossEPG_SFMenuEpg(Screen):
	def __init__(self, session):
		if (getDesktop(0).size().width() < 800):
			skin = "%s/skins/menu_sd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		else:
			skin = "%s/skins/menu_hd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		f = open(skin, "r")
		self.skin = f.read()
		f.close()
		Screen.__init__(self, session)

		self.config = CrossEPG_Config()
		self.config.load()
		self.patchtype = getEPGPatchType()

		l = []
		l.append(self.buildListEntry(_("Force csv import now"), "csv.png"))
		l.append(self.buildListEntry(_("Force epg.dat conversion now"), "conversion.png"))
		l.append(self.buildListEntry(_("Force epg reload"), "reload.png"))

		self["list"] = List(l)
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

		self.onFirstExecBegin.append(self.setTitleWithVerion)
		
		if self.config.configured == 0:
			self.onFirstExecBegin.append(self.openSetup)

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image));
		return((pixmap, description))

	def openSetup(self):
		self.session.open(CrossEPG_SetupSF)
			
	def setTitleWithVerion(self):
		try:
			global version
			self.setTitle("CrossEPG Panel")
		except Exception, e:
			self.setTitle("CrossEPG Panel")

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			self.importer()
		elif index == 1:
			self.converter()
		elif index == 2:
			self.loader()
		
	def quit(self):
		self.close()

	def downloader(self):
		self.config.load()
		self.session.openWithCallback(self.downloadCallback, CrossEPG_Downloader, self.config.providers)

	def downloadCallback(self, ret):
		if ret:
			if self.config.csv_import_enabled == 1:
				self.importer()
			else:
				if self.patchtype != 3:
					self.converter()
				else:
					self.loader()

	def importer(self):
		self.session.openWithCallback(self.importerCallback, CrossEPG_Importer)

	def importerCallback(self, ret):
		if ret:
			if self.patchtype != 3:
				self.converter()
			else:
				self.loader()

	def converter(self):
		self.session.openWithCallback(self.converterCallback, CrossEPG_Converter)

	def converterCallback(self, ret):
		if ret:
			if self.patchtype != -1:
				self.loader()
			else:
				if self.config.download_manual_reboot:
					from Screens.Standby import TryQuitMainloop
					self.session.open(TryQuitMainloop, 3)

	def loader(self):
		self.session.open(CrossEPG_Loader)

class CrossEPG_SFMenuInfo(Screen):
	def __init__(self, session):
		if (getDesktop(0).size().width() < 800):
			skin = "%s/skins/menu_sd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		else:
			skin = "%s/skins/menu_hd.xml" % os.path.dirname(sys.modules[__name__].__file__)
		f = open(skin, "r")
		self.skin = f.read()
		f.close()
		Screen.__init__(self, session)

		self.config = CrossEPG_Config()
		self.config.load()
		self.patchtype = getEPGPatchType()

		l = []
		l.append(self.buildListEntry(_("Info about database"), "dbinfo.png"))
		l.append(self.buildListEntry(_("About"), "about.png"))

		self["list"] = List(l)
		self["setupActions"] = ActionMap(["SetupActions"],
		{
			"cancel": self.quit,
			"ok": self.openSelected,
		}, -2)

		self.onFirstExecBegin.append(self.setTitleWithVerion)
		
		if self.config.configured == 0:
			self.onFirstExecBegin.append(self.openSetup)

	def buildListEntry(self, description, image):
		pixmap = LoadPixmap(cached=True, path="%s/images/%s" % (os.path.dirname(sys.modules[__name__].__file__), image));
		return((pixmap, description))

	def openSetup(self):
		self.session.open(CrossEPG_SetupSF)
			
	def setTitleWithVerion(self):
		try:
			global version
			self.setTitle("CrossEPG - %s" % version)
		except Exception, e:
			self.setTitle("CrossEPG - unknow version")

	def openSelected(self):
		index = self["list"].getIndex()
		if index == 0:
			self.session.open(CrossEPG_InfoSF)
		elif index == 1:
			self.session.open(CrossEPG_AboutSF)
		
	def quit(self):
		self.close()

	def downloader(self):
		self.config.load()
		self.session.openWithCallback(self.downloadCallback, CrossEPG_Downloader, self.config.providers)

	def downloadCallback(self, ret):
		if ret:
			if self.config.csv_import_enabled == 1:
				self.importer()
			else:
				if self.patchtype != 3:
					self.converter()
				else:
					self.loader()

	def importer(self):
		self.session.openWithCallback(self.importerCallback, CrossEPG_Importer)

	def importerCallback(self, ret):
		if ret:
			if self.patchtype != 3:
				self.converter()
			else:
				self.loader()

	def converter(self):
		self.session.openWithCallback(self.converterCallback, CrossEPG_Converter)

	def converterCallback(self, ret):
		if ret:
			if self.patchtype != -1:
				self.loader()
			else:
				if self.config.download_manual_reboot:
					from Screens.Standby import TryQuitMainloop
					self.session.open(TryQuitMainloop, 3)

	def loader(self):
		self.session.open(CrossEPG_Loader)
