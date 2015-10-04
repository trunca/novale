from Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest, MultiContentEntryPixmapAlphaBlend
from Console import SFConsole
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import gettext
from Components.Language import language
from os import environ
import os
import sys
from Screens.MessageBox import MessageBox
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigIP, ConfigDateTime, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Components.Sources.StaticText import StaticText
from enigma import eListboxPythonMultiContent, gFont, eEnv, getDesktop, pNavigation
from os import path as os_path, system as os_system, unlink, stat, mkdir, popen, makedirs, listdir, access, rename, remove, W_OK, R_OK, F_OK
from Plugins.SystemPlugins.CrossEPG.crossepg_downloader import CrossEPG_Downloader
from Plugins.SystemPlugins.CrossEPG.crossepg_converter import CrossEPG_Converter
from Plugins.SystemPlugins.CrossEPG.crossepg_importer import CrossEPG_Importer
from Plugins.SystemPlugins.CrossEPG.crossepglib import *
from Plugins.SystemPlugins.CrossEPG.crossepg_loader import CrossEPG_Loader

class mainSFPanel(Screen):
	skin = """
		<screen name="mainSFPanel" position="209,48" size="865,623" title="SFpanel" flags="wfNoBorder" backgroundColor="transparent">	
    <ePixmap pixmap="SF_HD/Bg_EPG_view.png" zPosition="-1" position="0,0" size="865,623" alphatest="on"/>
    <ePixmap pixmap="SF_HD/menu/ico_title_Setup.png" position="32,41" size="40,40" alphatest="blend" transparent="1"/>
    <eLabel text="SFpanel" position="90,50" size="600,32" font="Semiboldit;32" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1"/>
    <ePixmap pixmap="SF_HD/icons/clock.png" position="750,55" zPosition="1" size="20,20" alphatest="blend"/>
    <widget source="global.CurrentTime" render="Label" position="770,57" zPosition="1" size="50,20" font="Regular;20" foregroundColor="#1c1c1c" backgroundColor="#27d9dee2" halign="right" transparent="1">
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <ePixmap pixmap="SF_HD/buttons/red.png" position="45,98" size="25,25" alphatest="blend"/>
    <widget source="key_red" render="Label" position="86,97" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="#1c1c1c" transparent="1"/>
    <ePixmap pixmap="SF_HD/border_menu1.png" position="60,140" zPosition="-1" size="342,370" transparent="1" alphatest="blend"/>
    <widget name="list" position="70,150" size="320,350" backgroundColor="#a7a7a7" itemHeight="50" transparent="1" />
    <widget name="sublist" position="410,150" size="320,350" backgroundColor="#27d9dee2" itemHeight="50" />
    <widget name="description" position="130,540" size="600,110" zPosition="1" font="Regular;22" halign="center" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1" />
    <ePixmap pixmap="/usr/share/enigma2/sfpanel/sel.png" position="65,528" size="60,600" alphatest="blend" transparent="1"/>
          
  </screen> """

	def __init__(self, session):
		Screen.__init__(self, session)
		
		Screen.setTitle(self, _("Sfpanel Menu"))

		self["key_red"] = StaticText(_("Close"))
		self["description"] = Label()
		self["summary_description"] = StaticText("")

		self.menu = 0
		self.list = []
		self["list"] = SFMenuList(self.list)
		self.sublist = []
		self["sublist"] = SFMenuSubList(self.sublist)
		self.selectedList = []
		self.onChangedEntry = []
		self["list"].onSelectionChanged.append(self.selectionChanged)
		self["sublist"].onSelectionChanged.append(self.selectionSubChanged)

		self["actions"] = ActionMap(["SetupActions","WizardActions","MenuActions","MoviePlayerActions"],
		{
			"red": self.keyred,
			"ok": self.ok,
			"back": self.keyred,
			"cancel": self.keyred,
			"left": self.goLeft,
			"right": self.goRight,
			"up": self.goUp,
			"down": self.goDown,
		}, -1)


		
		self.SFmenu()
		self.selectedList = self["list"]
		self.selectionChanged()
		self.onLayoutFinish.append(self.layoutFinished)

	def createSummary(self):
		pass

	def layoutFinished(self):
		self["sublist"].selectionEnabled(0)

	def selectionChanged(self):
		if self.selectedList == self["list"]:
			item = self["list"].getCurrent()
			if item:
				self["description"].setText(_(item[4]))
				self["summary_description"].text = item[0]
				self.okList()

	def selectionSubChanged(self):
		if self.selectedList == self["sublist"]:
			item = self["sublist"].getCurrent()
			if item:
				self["description"].setText(_(item[3]))
				self["summary_description"].text = item[0]

	def goLeft(self):
		if self.menu <> 0:
			self.menu = 0
			self.selectedList = self["list"]
			self["list"].selectionEnabled(1)
			self["sublist"].selectionEnabled(0)
			self.selectionChanged()

	def goRight(self):
		if self.menu == 0:
			self.menu = 1
			self.selectedList = self["sublist"]
			self["sublist"].moveToIndex(0)
			self["list"].selectionEnabled(0)
			self["sublist"].selectionEnabled(1)
			self.selectionSubChanged()

	def goUp(self):
		self.selectedList.up()
		
	def goDown(self):
		self.selectedList.down()
		
	def keyred(self):
		self.close()


######## Menu principal ##############################
	def SFmenu(self):
		self.menu = 0
		self.list = []
		self.oldlist = []
		self.list.append(SFMenuEntryComponent("Softcam",_("Start/stop/select cam"),_("Start/stop/select your cam, You need to install first a softcam")))
		self.list.append(SFMenuEntryComponent("Backup",_("Realizar backup de tu receptor"),_("Realizar backup de tu receptor en unidad montada HDD o USB")))
		self.list.append(SFMenuEntryComponent("Software Manager",_("Actualizar, instalar tu receptor"),_("Actualizar, flashear on line, instalar paquetes en tu receptor")))
		self.list.append(SFMenuEntryComponent("EPG",_("Actualizar EPG"),_("Actualizar lista de eventos epg de nuestro receptor")))
		self.list.append(SFMenuEntryComponent("Utilities",_("utilities receptor"),_("Utilidades varias para nuestro receptor")))
		self.list.append(SFMenuEntryComponent("Multimedia",_("Configuracion multimedia"),_("Convierte tu receptor en un centro multimedia")))
		self.list.append(SFMenuEntryComponent("Panel Drivers",_("Install drivers"),_("install drivers for receptor")))
		self.list.append(SFMenuEntryComponent("Info Panel",_("Informacion receptor"),_("Informacion sobre receptor")))
		self.list.append(SFMenuEntryComponent("Utilities Skin",_("Opciones extra skin"),_("Descarga skin part, configuracion weather")))
		self["list"].l.setList(self.list)

######## Menu softcam ##############################
	def SFsoftcam(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("Softcam Panel",_("Control your Softcams"),_("Use the Softcam Panel to control your Cam. This let you start/stop/select a cam")))
		self.sublist.append(SFSubMenuEntryComponent(_("card-Panel Setup"),_("Control your Cardserver"),_('Use the Cardserver Panel to control your Cam. This let you start/stop/select a cam')))
		self.sublist.append(SFSubMenuEntryComponent(_("CCcam suite"),_("Informacion CCcam emu"),_('Acceda a toda la informacion de su emuladora cccam')))
		self.sublist.append(SFSubMenuEntryComponent(_("Oscam suite"),_("Informacion oscam emu"),_('Acceda a toda la informacion de su emuladora oscam')))
		self.sublist.append(SFSubMenuEntryComponent(_("Gbox suite"),_("Informacion Gbox emu"),_('Acceda a toda la informacion de su emuladora gbox o mbox')))
		self["sublist"].l.setList(self.sublist)
######## Menu backup ##############################
	def SFBackup(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("Backup HDD",_("Realizar backup hdd"),_("Realize copia de seguridad de su imagen en unidad HDD")))
		self.sublist.append(SFSubMenuEntryComponent(_("Backup USB"),_("Realizar backup usb"),_('Realize copia de seguridad de su imagen en unidad USB')))
		self["sublist"].l.setList(self.sublist)
######## Menu sofware manager ##############################
	def SFSoftwareManager(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("Flash online",_("Instalar imagen en tu receptor"),_("Instalar imagen desde ubicacion red o desde ubicacion local")))
		self.sublist.append(SFSubMenuEntryComponent("Software Update",_("Online software update"),_("Check/Install online updates (you must have a working internet connection)")))
		self.sublist.append(SFSubMenuEntryComponent("install-extensions",_("Manage extensions"),_("Manage extensions or plugins for your receiver)")))
		self.sublist.append(SFSubMenuEntryComponent("software-restore",_("Software restore"),_("Restore your receiver with a new firmware)")))
		self.sublist.append(SFSubMenuEntryComponent("system-backup",_("Backup system settings"),_("Backup your receiver settings")))
		self.sublist.append(SFSubMenuEntryComponent("system-restore",_("Restore system settings"),_("Restore your receiver settings")))
		self.sublist.append(SFSubMenuEntryComponent("ipkg-install",_("Install local extension"),_("Scan for local extensions and install them")))
		self.sublist.append(SFSubMenuEntryComponent("Software Manager Setup",_("Manage your online update files"),_("Here you can select which files should be updated with a online update")))
		self["sublist"].l.setList(self.sublist)
######## Menu epg ##############################
	def SFEPG(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("Setup Epg",_("Configure CrossEPG"),_("Configure parametros de crossepg")))
		self.sublist.append(SFSubMenuEntryComponent("Epg Providers",_("Configure epg provider"),_("Seleccione epg provider para actualizacion")))
		self.sublist.append(SFSubMenuEntryComponent("Epg Tools",_("Herramientas epg"),_("acceda a herramientas epg")))
		self.sublist.append(SFSubMenuEntryComponent("Download now",_("Download"),_("descarga nueva")))
		self.sublist.append(SFSubMenuEntryComponent("Information",_("About epg"),_("information epg")))
		self["sublist"].l.setList(self.sublist)
######## Menu utilities ##############################
	def SFUtilities(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("Mount Manager",_("Montar unidades"),_("Monte sus unidades hdd, usb, en su receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Cron Manager",_("Cron Manager"),_("Configure la ejecucion de procesos")))
		self.sublist.append(SFSubMenuEntryComponent("Clean memory",_("libere memoria"),_("Pulse para libearia memoria ram de su receptor")))
		self.sublist.append(SFSubMenuEntryComponent("password changer",_("Cambiar password"),_("Cambie el pasword root de su receptor")))
		self.sublist.append(SFSubMenuEntryComponent("password reset",_("Resetea tu password"),_("elimine el pasword root de su receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Internet speed test",_("Velocidad conexion"),_("Testee la velocidad de conexion a internet de su receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Swap create",_("Cree particiones swap"),_("Cree particiones swap en la unidad montada de su receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Update feeds",_("Actualizar feed"),_("Actualizar lista de feed del servidor")))
		self.sublist.append(SFSubMenuEntryComponent("Upgrade feeds",_("Upgrade feed"),_("Upgrade feed lista servidor")))
		self.sublist.append(SFSubMenuEntryComponent("Crashlog",_("Crashlog view"),_("Crashlog view")))
		self["sublist"].l.setList(self.sublist)
######## Menu Multimedia ##############################
	def SFMultimedia(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("Mediatomb",_("Configure Mediatomb"),_("Configure acceso al receptor a traves de Mediatomb")))
		self.sublist.append(SFSubMenuEntryComponent("Xupnpd",_("Configure Xupnpd"),_("Configure acceso al receptor a traves de Xupnpd")))
		self.sublist.append(SFSubMenuEntryComponent("Udpxy",_("Configure Udpxy"),_("Configure acceso al receptor a traves de Udpxy")))
		self.sublist.append(SFSubMenuEntryComponent("Tunerserver Panel",_("Create channel list"),_("Create channel list mu3 format")))
		self["sublist"].l.setList(self.sublist)

######## Menu drivers ##############################
	def SFdrivers(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("TDT drivers",_("Install drivers"),_("Install drivers tdt usb")))
		self.sublist.append(SFSubMenuEntryComponent("Wifi drivers",_("Install drivers"),_("Install drivers wifi usb")))
		self["sublist"].l.setList(self.sublist)
######## Menu infopanel ##############################
	def SFinfopanel(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("Check memory",_("Check memory"),_("Check memory usage receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Proc information",_("Proc information"),_("Proc information receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Ecm information",_("Ecm information"),_("Ecm information for emu")))
		self.sublist.append(SFSubMenuEntryComponent("Driver version",_("Driver version"),_("Driver version install receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Box uptime",_("Box uptime"),_("Box uptime receptor")))
		self.sublist.append(SFSubMenuEntryComponent("Public IP",_("Public IP"),_("view Public IP")))
		self["sublist"].l.setList(self.sublist)
######## Menu SKIN ##############################
	def SFskin(self):
		self.sublist = []
		self.sublist.append(SFSubMenuEntryComponent("weather",_("Configuracion tiempo"),_("Configure tu zona weather")))
		self.sublist.append(SFSubMenuEntryComponent("skinpart",_("Install skin part"),_("Install skin part for skin SF_HD")))
		self["sublist"].l.setList(self.sublist)


	def ok(self):
		if self.menu > 0:
			self.okSubList()
		else:
			self.goRight()
#####################################################################
######## Seleccion menu lista ##############################
#####################################################################
			
	def okList(self):
		item = self["list"].getCurrent()

######## Select sofcam ##############################
		if item[0] == _("Softcam"):
			self.SFsoftcam()
		elif item[0] == _("Backup"):
			self.SFBackup()
		elif item[0] == _("Software Manager"):
			self.SFSoftwareManager()
		elif item[0] == _("EPG"):
			self.SFEPG()
		elif item[0] == _("Utilities"):
			self.SFUtilities()
		elif item[0] == _("Multimedia"):
			self.SFMultimedia()
		elif item[0] == _("Panel Drivers"):
			self.SFdrivers()
		elif item[0] == _("Info Panel"):
			self.SFinfopanel()
		elif item[0] == _("Utilities Skin"):
			self.SFskin()
		self["sublist"].selectionEnabled(0)
#####################################################################
######## Seleccion menu sublista ##############################
#####################################################################
			
	def okSubList(self):
		item = self["sublist"].getCurrent()

######## Seleccion softcam menu ##############################
		if item[0] == _("Softcam Panel"):
			import SoftPanel
            		self.session.open(SoftPanel.SoftcamSetupSF)
		elif item[0] == _("card-Panel Setup"):
			import CardPanel
            		self.session.open(CardPanel.CardserverSetup)
		elif item[0] == _("CCcam suite"):
            		sys.path.append('/usr/lib/enigma2/python/Screens/SFextra/CCcamInfo')
	    		import cccaminfo
            		self.session.open(cccaminfo.CCcamInfoMain)
		elif item[0] == _("Oscam suite"):
            		sys.path.append('/usr/lib/enigma2/python/Screens/SFextra/OscamInfo')
	    		import oscaminfo
            		self.session.open(oscaminfo.OscamInfoMenu)
		elif item[0] == _("Gbox suite"):
           	        sys.path.append('/usr/lib/enigma2/python/Screens/SFextra/GboxSuite')
	   	        import gboxsuite
            		self.session.open(gboxsuite.GboxSuiteMainMenu)

######## Seleccion backup menu ##############################
		if item[0] == _("Backup HDD"):
			import Backup
			self.session.open(Backup.BackupPanelhdd)
		elif item[0] == _("Backup USB"):
			import Backup
			self.session.open(Backup.BackupPanel)
######## Seleccion sofware manager ##############################
		if item[0] == _("Flash online"):
			from Flash import FlashOnline
            		self.session.open(FlashOnline)
		elif item[0] == _("Software Update"):
			import SoftwareUpdate
			self.session.open(SoftwareUpdate.UpdatePlugin)
		elif item[0] == _("install-extensions"):
			from Plugins.SystemPlugins.SoftwareManager.plugin import PluginManager
			self.session.open(PluginManager)
		elif item[0] == _("software-restore"):
			from Plugins.SystemPlugins.SoftwareManager.ImageWizard import ImageWizard
			self.session.open(ImageWizard)
		elif item[0] == _("system-backup"):
			from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen, RestoreScreen, BackupSelection, getBackupFilename
			self.session.openWithCallback(self.backupDone,BackupScreen, runBackup = True)
		elif item[0] == _("system-restore"):
					from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupSelection, RestoreMenu, BackupScreen, RestoreScreen, getBackupPath, getBackupFilename
					self.backuppath = getBackupPath()
					self.backupfile = getBackupFilename()
					self.fullbackupfilename = self.backuppath + "/" + self.backupfile
					if os_path.exists(self.fullbackupfilename):
						self.session.openWithCallback(self.startRestore, MessageBox, _("Are you sure you want to restore the backup?\nYour receiver will restart after the backup has been restored!"))
					else:
						self.session.open(MessageBox, _("Sorry, no backups found!"), MessageBox.TYPE_INFO, timeout = 10)
		elif item[0] == _("ipkg-install"):
					try:
						from Plugins.Extensions.MediaScanner.plugin import main
						main(self.session)
					except:
						self.session.open(MessageBox, _("Sorry, %s has not been installed!") % ("MediaScanner"), MessageBox.TYPE_INFO, timeout = 10)
		elif item[0] == _("Software Manager Setup"):
			from Plugins.SystemPlugins.SoftwareManager.plugin import SoftwareManagerSetup
			self.session.open(SoftwareManagerSetup)
######## Seleccion epg menu ##############################
		if item[0] == _("Setup Epg"):
			from Plugins.SystemPlugins.CrossEPG.crossepg_setup import CrossEPG_SetupSF
            		self.session.open(CrossEPG_SetupSF)
		elif item[0] == _("Epg Providers"):
			import SFepg
			self.session.open(SFepg.CrossEPG_SFMenuProviders)
		elif item[0] == _("Epg Tools"):
			import SFepg
			self.session.open(SFepg.CrossEPG_SFMenuEpg)
		elif item[0] == _("Download now"):
			self.patchtype = getEPGPatchType()
			self.config = CrossEPG_Config()
			self.config.load()
            		self.config.deleteLog()
            		self.downloader()
		elif item[0] == _("Information"):
			import SFepg
            		self.session.open(SFepg.CrossEPG_SFMenuInfo)
######## Seleccion utilities ##############################
		if item[0] == _("Mount Manager"):
			import Mount
           		self.session.open(Mount.HddMount)
		elif item[0] == _("Cron Manager"):
            		import Cron
            		self.session.open(Cron.CronManager)
		elif item[0] == _("Clean memory"):
			self.clear()
		elif item[0] == _("password changer"):
			import Password
            		self.session.open(Password.PasswordChanger)
		elif item[0] == _("password reset"):
			self.passreset()
		elif item[0] == _("Internet speed test"):
			self.session.open(SFConsole, title=_('Running internet speed test'), cmdlist=['python /usr/lib/enigma2/python/Screens/SpeedTest.pyo'])
		elif item[0] == _("Swap create"):
	    		import SFextra
           		self.session.open(SFextra.SwapScreen2)
		elif item[0] == _("Update feeds"):
			self.updatefeeds()
		elif item[0] == _("Upgrade feeds"):
			import sfupgrade
			self.session.open(sfupgrade.SFsearchupgrade)
		elif item[0] == _("Crashlog"):
			import SFextra
			self.session.open(SFextra.CrashLogScreen)



######## Seleccion Multimedia ##############################
		if item[0] == _("Mediatomb"):
			import Mediatomb
            		self.session.open(Mediatomb.MediatombPanel)
		elif item[0] == _("Xupnpd"):
			import Mediatomb
            		self.session.open(Mediatomb.xupnpdpanel)
		elif item[0] == _("Udpxy"):
			import Mediatomb
            		self.session.open(Mediatomb.udpxypanel)
		elif item[0] == _("Tunerserver Panel"):
			import Tuner
            		self.session.open(Tuner.TunerServer)
######## Seleccion drivers ##############################
		if item[0] == _("TDT drivers"):
			import SFextra
            		self.session.open(SFextra.tdtpanel)
		elif item[0] == _("Wifi drivers"):
			import SFextra
            		self.session.open(SFextra.wifipanel)

######## Seleccion infopanel ##############################
		if item[0] == _("Check memory"):
			self.session.open(SFConsole, title=_('Check memory usage'), cmdlist=['cat /proc/meminfo'])
		elif item[0] == _("Proc information"):
			self.session.open(SFConsole, title=_('Proc information'), cmdlist=['cat /proc/stb/info/boxtype & cat /proc/stb/info/gbmodel & cat /proc/stb/info/model & cat /proc/stb/info/chipset & cat /proc/stb/info/version'])
		elif item[0] == _("Ecm information"):
			import SFextra
            		self.session.open(SFextra.SFecminfo)
		elif item[0] == _("Driver version"):
			self.session.open(SFConsole, title=_('Driver version'), cmdlist=['opkg list-installed | grep dvb-mod'])
		elif item[0] == _("Box uptime"):
			self.session.open(SFConsole, title=_('Box uptime'), cmdlist=['uptime'])
		elif item[0] == _("Public IP"):
			self.miip()

######## Seleccion skin ##############################
		if item[0] == _("weather"):
			from Plugins.Extensions.WeatherPlugin.plugin import MSNWeatherPlugin
            		self.session.open(MSNWeatherPlugin)
		elif item[0] == _("skinpart"):
			import SFextra
            		self.session.open(SFextra.skinpart)
		
######## SOFTWARE HERRAMIENTAS #######################
	def backupfiles_choosen(self, ret):
		config.plugins.configurationbackup.backupdirs.save()
		config.plugins.configurationbackup.save()
		config.save()

	def backupDone(self,retval = None):
		if retval is True:
			self.session.open(MessageBox, _("Backup done."), MessageBox.TYPE_INFO, timeout = 10)
		else:
			self.session.open(MessageBox, _("Backup failed."), MessageBox.TYPE_INFO, timeout = 10)

	def startRestore(self, ret = False):
		if (ret == True):
			self.exe = True
			self.session.open(RestoreScreen, runRestore = True)

#############software epg################################
	def downloader(self):
        	self.config.load()
        	self.session.openWithCallback(self.downloadCallback, CrossEPG_Downloader, self.config.providers)

    	def downloadCallback(self, ret):
        	if ret:
            		if self.config.csv_import_enabled == 1:
                		self.importer()
            		elif self.patchtype != 3:
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
            	elif self.config.download_manual_reboot:
                	from Screens.Standby import TryQuitMainloop
                	self.session.open(TryQuitMainloop, 3)

    	def loader(self):
        	self.session.open(CrossEPG_Loader)

#############software utilidades################################

	def clear(self):
		os.system("sync ; echo 3 > /proc/sys/vm/drop_caches")
		os.system("free | awk '/Mem:/ {print int(100*$3/$2) ;}' >/tmp/.memory")
		f = open("/tmp/.memory")
		mused = f.readline()
		f.close()
		self.mbox = self.session.open(MessageBox,_("free memory after execution: %s ") % (mused), MessageBox.TYPE_INFO, timeout = 20 )

	def passreset(self):
		os.system("passwd -d root")
		self.mbox = self.session.open(MessageBox,_("your password has been deleted"), MessageBox.TYPE_INFO, timeout = 10 )
        def updatefeeds(self):
                os.system("opkg update")
                self.mbox = self.session.open(MessageBox,_("Lista feed actualizada"), MessageBox.TYPE_INFO, timeout = 10 )

#############software infopanel################################

    	def miip(self):
		os.popen("wget -qO /tmp/.mostrarip http://icanhazip.com/")
		f = open("/tmp/.mostrarip")
		mostrarip = f.readline()
		f.close()
		self.mbox = self.session.open(MessageBox,_("public your ip is: %s") % (mostrarip), MessageBox.TYPE_INFO, timeout = 10 )
######## creacion menu lista #######################
def SFMenuEntryComponent(name, description, long_description = None, width=540):
	pngname = name.replace(" ","_") 
	png = LoadPixmap("/usr/share/enigma2/sfpanel/" + pngname + ".png")
	if png is None:
		png = LoadPixmap("/usr/share/enigma2/sfpanel/default.png")

	screenwidth = getDesktop(0).size().width()
	if screenwidth and screenwidth == 1920:
		return [
			_(name),
			MultiContentEntryText(pos=(90, 10), size=(width-90, 38), font=0, text = _(name)),
			MultiContentEntryText(pos=(90, 39), size=(width-90, 26), font=1, text = _(description)),
			MultiContentEntryPixmapAlphaBlend(pos=(15, 10), size=(60, 60), png = png),
			_(long_description),
		]
	else:
		return [
			_(name),
			MultiContentEntryText(pos=(60, 5), size=(width-60, 25), font=0, text = _(name)),
			MultiContentEntryText(pos=(60, 26), size=(width-60, 17), font=1, text = _(description)),
			MultiContentEntryPixmapAlphaBlend(pos=(10, 5), size=(40, 40), png = png),
			_(long_description),
		]

def SFSubMenuEntryComponent(name, description, long_description = None, width=540):
	screenwidth = getDesktop(0).size().width()
	if screenwidth and screenwidth == 1920:
		return [
			_(name),
			MultiContentEntryText(pos=(15, 8), size=(width-15, 38), font=0, text = _(name)),
			MultiContentEntryText(pos=(15, 39), size=(width-15, 26), font=1, text = _(description)),
			_(long_description),
		]
	else:
		return [
			_(name),
			MultiContentEntryText(pos=(10, 5), size=(width-10, 25), font=0, text = _(name)),
			MultiContentEntryText(pos=(10, 26), size=(width-10, 17), font=1, text = _(description)),
			_(long_description),
		]

class SFMenuList(MenuList):
	def __init__(self, list, enableWrapAround=True):
		MenuList.__init__(self, list, enableWrapAround, eListboxPythonMultiContent)
		screenwidth = getDesktop(0).size().width()
		if screenwidth and screenwidth == 1920:
			self.l.setFont(0, gFont("Regular", 30))
			self.l.setFont(1, gFont("Regular", 21))
			self.l.setItemHeight(75)
		else:
			self.l.setFont(0, gFont("Regular", 20))
			self.l.setFont(1, gFont("Regular", 14))
			self.l.setItemHeight(50)

class SFMenuSubList(MenuList):
	def __init__(self, sublist, enableWrapAround=True):
		MenuList.__init__(self, sublist, enableWrapAround, eListboxPythonMultiContent)
		screenwidth = getDesktop(0).size().width()
		if screenwidth and screenwidth == 1920:
			self.l.setFont(0, gFont("Regular", 30))
			self.l.setFont(1, gFont("Regular", 21))
			self.l.setItemHeight(75)
		else:
			self.l.setFont(0, gFont("Regular", 20))
			self.l.setFont(1, gFont("Regular", 14))
			self.l.setItemHeight(50)
		



