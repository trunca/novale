from Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Components.Pixmap import Pixmap
from enigma import ePicLoad
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.config import config, getConfigListEntry, ConfigText, ConfigPassword, ConfigClock, ConfigIP, ConfigDateTime, ConfigSelection, ConfigSubsection, ConfigYesNo, configfile, NoSave
from Console import SFConsole
from Components.Sources.StaticText import StaticText
from Components.Console import Console as iConsole
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import gettext
from Components.Language import language
from Tools.Directories import fileExists, pathExists, resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from os import environ
import os
import sys
from Screens.MessageBox import MessageBox
import time
from Components.ScrollLabel import ScrollLabel
from Screens.Standby import TryQuitMainloop
from enigma import ePoint, eTimer, getDesktop, iServiceInformation
import subprocess, threading
import uuid
import urllib2
from urllib2 import urlopen
from Screens.Standby import TryQuitMainloop

if os.path.isfile('%s%sbitratecalc.so' % (resolveFilename(SCOPE_PLUGINS), "SFteam/")):
	from Plugins.SFteam.bitratecalc import eBitrateCalculator
	binary_file = True
else:
	binary_file = False

def mountp():
	pathmp = []
	if fileExists("/proc/mounts"):
		for line in open("/proc/mounts"):
			if '/dev/sd' in line or '/dev/disk/by-uuid/' in line or '/dev/mmc' in line:
				pathmp.append(line.split()[1].replace('\\040', ' ') + "/")
	pathmp.append("/usr/share/enigma2/")
	pathmp.append("/tmp/")
	return pathmp

def remove_line(filename, what):
	if fileExists(filename):
		file_read = open(filename).readlines()
		file_write = open(filename, 'w')
		for line in file_read:
			if what not in line:
				file_write.write(line)
		file_write.close()
def logging(line):
	log_file = open('/tmp/sfpanel.log', 'a')
	log_file.write(line)
	log_file.close()

config.crashpath = ConfigSelection(default = '/media/hdd/', choices = [
		('/media/hdd/', _('/media/hdd')),
		('/home/root/', _('/home/root')),
		('/home/root/logs/', _('/home/root/logs')),
		('/tmp/', _('/tmp')),
])


########fin config swap#########

#####swap############

class SwapScreen2(Screen):
	skin = """
		<screen name="SwapScreen2" position="center,160" size="750,370" title="Swap on USB/HDD">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/share/enigma2/YADS-HD/buttons/button_red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 1), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 2), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Swap on USB/HDD"))
		self.iConsole = iConsole()
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Menu,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.Menu()
		
	def del_fstab_swap(self, result, retval, extra_args):
		if retval is 0:
			remove_line('/etc/fstab', 'swap')
		
	def Menu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path="/usr/share/enigma2/sfpanel/swapmini.png")
		minisonpng = LoadPixmap(cached=True, path="/usr/share/enigma2/sfpanel/swapminion.png")
		if self.is_zram():
			if fileExists("/proc/swaps"):
				for line in open("/proc/swaps"):
					if "media" in line:
						self.iConsole.ePopen("swapoff %s" % (line.split()[0]), self.del_fstab_swap)
			self.list.append((_("Zram swap is on"), _("press Close for Exit"), minispng, 'zram'))
		else:
			for line in mountp():
				#if line not in "/usr/share/enigma2/" or line not in "/tmp/":
				if "/tmp/" not in line and "/usr/share/enigma2/" not in line:
					try:
						if self.swapiswork() in line:
							self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minisonpng, line))
						else:
							self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
					except:
						self.list.append((_("Manage Swap on %s") % line, _("Start, Stop, Create, Remove Swap file"), minispng, line))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.MenuDo, "cancel": self.close}, -1)
	
	def is_zram(self):
		if fileExists("/proc/swaps"):
			for line in open("/proc/swaps"):
				if "zram0" in line:
					return True
		return False
		
	def swapiswork(self):
		if fileExists("/proc/swaps"):
			for line in open("/proc/swaps"):
				if "media" in line:
					return line.split()[0][:-9]
		else:
			return " "
		
	def MenuDo(self):
		try:
			if "zram" in self["menu"].getCurrent()[3]:
				return
			swppath = self["menu"].getCurrent()[3] + "swapfile"
		except:
			return
		self.session.openWithCallback(self.Menu,SwapScreen, swppath)
	
	def exit(self):
		self.close()
######################################################################################
class SwapScreen(Screen):
	skin = """
	<screen name="SwapScreen" position="center,160" size="750,370" title="Swap on USB/HDD">
	<ePixmap position="20,358" zPosition="1" size="170,2" pixmap="/usr/share/enigma2/YADS-HD/buttons/button_red.png" alphatest="blend" />
	<widget source="key_red" render="Label" position="20,328" zPosition="2" size="170,30" font="Regular;20" halign="center" valign="center" backgroundColor="background" foregroundColor="foreground" transparent="1" />
	<widget source="menu" render="Listbox" position="20,20" size="710,253" scrollbarMode="showOnDemand">
	<convert type="TemplatedMultiContent">
	{"template": [
		MultiContentEntryText(pos = (70, 2), size = (580, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
		MultiContentEntryText(pos = (80, 29), size = (580, 18), font=1, flags = RT_HALIGN_LEFT, text = 2), # index 3 is the Description
		MultiContentEntryPixmapAlphaTest(pos = (5, 5), size = (50, 40), png = 3), # index 4 is the pixmap
			],
	"fonts": [gFont("Regular", 23),gFont("Regular", 16)],
	"itemHeight": 50
	}
			</convert>
		</widget>
	</screen>"""

	def __init__(self, session, swapdirect):
		self.swapfile = swapdirect
		self.session = session
		Screen.__init__(self, session)
		self.setTitle(_("Swap on USB/HDD"))
		self.iConsole = iConsole()
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.CfgMenuDo,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
		})
		self["key_red"] = StaticText(_("Close"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()


	def isSwapPossible(self):
		for line in open("/proc/mounts"):
			fields= line.rstrip('\n').split()
			if fields[1] == "%s" % self.swapfile[:-9]:
				if fields[2] == 'ext2' or fields[2] == 'ext3' or fields[2] == 'ext4' or fields[2] == 'vfat':
					return True
				else:
					return False
		return False
		
	def isSwapRun(self):
		if fileExists('/proc/swaps'):
			for line in open('/proc/swaps'):
				if self.swapfile in line:
					return True
			return False
		else:
			return False
			
	def isSwapSize(self):
		if fileExists(self.swapfile):
			swapsize = os.path.getsize(self.swapfile) / 1048576
			return ("%sMb" % swapsize)
		else:
			return ("N/A Mb")

	def createSwapFile(self, size):
		self.session.openWithCallback(self.CfgMenu, create_swap, self.swapfile, size)

	def removeSwapFle(self):
		self.iConsole.ePopen("rm -f %s" % self.swapfile, self.info_mess, _("Swap file removed"))

	def info_mess(self, result, retval, extra_args):
		self.setTitle(_("Swap on USB/HDD"))
		if retval is 0:
			self.mbox = self.session.open(MessageBox,extra_args, MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,_("Failure..."), MessageBox.TYPE_INFO, timeout = 6)
		self.CfgMenu()

	def offSwapFile_step1(self):
		remove_line('/etc/fstab', 'swap')
		self.iConsole.ePopen("swapoff %s" % self.swapfile, self.info_mess, _("Swap file stoped"))

	def onSwapFile_step1(self):
		self.iConsole.ePopen("swapoff %s" % self.swapfile, self.onSwapFile_step2)
		
	def onSwapFile_step2(self, result, retval, extra_args):
		remove_line('/etc/fstab', 'swap')
		with open('/etc/fstab', 'a') as fsatb_file:
			fsatb_file.write('%s/swapfile swap swap defaults 0 0\n' % self.swapfile[:10])
			fsatb_file.close()
		self.iConsole.ePopen("swapon %s" % self.swapfile, self.info_mess,_("Swap file started"))

	def CfgMenu(self):
		self.list = []
		minispng = LoadPixmap(cached=True, path="/usr/share/enigma2/sfpanel/swapmini.png")
		minisonpng = LoadPixmap(cached=True, path="/usr/share/enigma2/sfpanel/swapminion.png")
		if self.isSwapPossible():
			if os.path.exists(self.swapfile):
				if self.isSwapRun():
					self.list.append((_("Swap off"),"5", (_("Swap on %s off (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minisonpng))
				else:
					self.list.append((_("Swap on"),"4", (_("Swap on %s on (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
					self.list.append((_("Remove swap"),"7",( _("Remove swap on %s (%s)") % (self.swapfile[7:10].upper(), self.isSwapSize())), minispng))
			else:
				self.list.append((_("Make swap"),"11", _("Make swap on %s (128MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"12", _("Make swap on %s (256MB)") % self.swapfile[7:10].upper(), minispng))
				self.list.append((_("Make swap"),"13", _("Make swap on %s (512MB)") % self.swapfile[7:10].upper(), minispng))
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.CfgMenuDo, "cancel": self.close}, -1)
			
	def CfgMenuDo(self):
		self.setTitle(_("Please wait"))
		if self.isSwapPossible() == 1:
			m_choice = self["menu"].getCurrent()[1]
			if m_choice is "4":
				self.onSwapFile_step1()
			elif m_choice is "5":
				self.offSwapFile_step1()
			elif m_choice is "11":
				self.createSwapFile("131072")
			elif m_choice is "12":
				self.createSwapFile("262144")
			elif m_choice is "13":
				self.createSwapFile("524288")
			elif m_choice is "7":
				self.removeSwapFle()
		self.CfgMenu()
			
	def exit(self):
		self.close()
######################################################################################
SKIN_CSW = """
<screen name="create_swap" position="center,140" size="625,30" title="Please wait">
  <widget source="status" render="Label" position="10,5" size="605,22" zPosition="2" font="Regular; 20" halign="center" transparent="2" />
</screen>"""

class create_swap(Screen):
	def __init__(self, session, swapfile, size):
		Screen.__init__(self, session)
		self.session = session
		self.skin = SKIN_CSW
		self.swapfile = swapfile
		self.size = size
		self.setTitle(_("Please wait"))
		self["status"] = StaticText()
		self.iConsole = iConsole()
		self["status"].text = _("Creating...")
		self.iConsole.ePopen("dd if=/dev/zero of=%s bs=1024 count=%s" % (self.swapfile, self.size), self.makeSwapFile)
		
	def makeSwapFile(self, result, retval, extra_args):
		if retval is 0:
			self.iConsole.ePopen("mkswap %s" % self.swapfile, self.info_mess)
		else:
			self["status"].text = _("Failure...")
			self.iConsole.ePopen("sleep 4", self.end_func)
			
	def info_mess(self, result, retval, extra_args):
		if retval is 0:
			self["status"].text = _("Success...")
			self.iConsole.ePopen("sleep 4", self.end_func)
		else:
			self["status"].text = _("Failure...")
			self.iConsole.ePopen("sleep 4", self.end_func)

	def end_func(self, result, retval, extra_args):
		self.close()
######################fin swap###################################
class tdtpanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="TDT Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'

    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('TDT Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Install drivers Siano'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Install drivers af9015'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Install drivers af9035'), 'copyepg.png'))
        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)
        self["key_red"] = StaticText(_("Close"))
	
    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)


    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
            self.siano()
        elif menuIndex == 1:
	    self.af9015()
        elif menuIndex == 2:
	    self.af9035()
            
    def siano(self):
	if os.popen("opkg list-installed | grep enigma2-plugin-drivers-dvb-usb-siano").read() == '':
            os.system("opkg install enigma2-plugin-drivers-dvb-usb-siano")
	    self.mbox = self.session.open(MessageBox,_("drivers siano has been install"), MessageBox.TYPE_INFO, timeout = 10 )
	else:
            self.mbox = self.session.open(MessageBox,_("drivers siano has installed"), MessageBox.TYPE_INFO, timeout = 10 )

    def af9015(self):
	if os.popen("opkg list-installed | grep enigma2-plugin-drivers-dvb-usb-af9015").read() == '':
            os.system("opkg install enigma2-plugin-drivers-dvb-usb-af9015")
	    self.mbox = self.session.open(MessageBox,_("drivers af9015 has been install"), MessageBox.TYPE_INFO, timeout = 10 )
	else:
            self.mbox = self.session.open(MessageBox,_("drivers af9015 has installed"), MessageBox.TYPE_INFO, timeout = 10 )

    def af9035(self):
	if os.popen("opkg list-installed | grep enigma2-plugin-drivers-dvb-usb-af9035").read() == '':
            os.system("opkg install enigma2-plugin-drivers-dvb-usb-af9035")
	    self.mbox = self.session.open(MessageBox,_("drivers af9035 has been install"), MessageBox.TYPE_INFO, timeout = 10 )
	else:
            self.mbox = self.session.open(MessageBox,_("drivers af9035 has installed"), MessageBox.TYPE_INFO, timeout = 10 )
            

    def quit(self):
        self.close()

class wifipanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Wifi Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'

    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Wifi Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Install drivers RTL8192cu'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Install drivers RT2800'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Install drivers RT2500'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Install drivers RT73'), 'copyepg.png'))
        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)
	self["key_red"] = StaticText(_("Close"))
	

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

   
    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
	    self.rtl8192cu()
        elif menuIndex == 1:
            self.rt2800usb()
        elif menuIndex == 2:
	    self.rt2500usb()
        elif menuIndex == 3:
	    self.rt73usb()
            
    def rtl8192cu(self):
	if os.popen("opkg list-installed | grep kernel-module-rtl8192cu").read() == '':
            os.system("opkg install kernel-module-rtl8192cu firmware-rtl8192cu")
	    self.mbox = self.session.open(MessageBox,_("drivers rtl8192cu has been install"), MessageBox.TYPE_INFO, timeout = 10 )
	else:
            self.mbox = self.session.open(MessageBox,_("drivers rtl8192cu has installed"), MessageBox.TYPE_INFO, timeout = 10 )

    def rt2800usb(self):
	if os.popen("opkg list-installed | grep kernel-module-rt2800usb").read() == '':
            os.system("opkg install kernel-module-rt2800usb")
	    self.mbox = self.session.open(MessageBox,_("drivers rt2800usb has been install"), MessageBox.TYPE_INFO, timeout = 10 )
	else:
            self.mbox = self.session.open(MessageBox,_("drivers rt2800usb has installed"), MessageBox.TYPE_INFO, timeout = 10 )

    def rt2500usb(self):
	if os.popen("opkg list-installed | grep kernel-module-rt2500usb").read() == '':
            os.system("opkg install kernel-module-rt2500usb")
	    self.mbox = self.session.open(MessageBox,_("drivers rt2500usb has been install"), MessageBox.TYPE_INFO, timeout = 10 )
	else:
            self.mbox = self.session.open(MessageBox,_("drivers rt2500usb has installed"), MessageBox.TYPE_INFO, timeout = 10 )

    def rt73usb(self):
	if os.popen("opkg list-installed | grep kernel-module-rt73usb").read() == '':
            os.system("opkg install kernel-module-rt73usb firmware-rt73")
	    self.mbox = self.session.open(MessageBox,_("drivers rt73usb has been install"), MessageBox.TYPE_INFO, timeout = 10 )
	else:
            self.mbox = self.session.open(MessageBox,_("drivers rt73usb has installed"), MessageBox.TYPE_INFO, timeout = 10 )



    def quit(self):
        self.close()

######################################################################################
class CrashLogScreen(Screen):
	skin = """
<screen name="CrashLogScreen" position="209,48" size="865,623" title="View or Remove Crashlog files" flags="wfNoBorder" backgroundColor="transparent">
	<ePixmap pixmap="SF_HD/Bg_EPG_view.png" zPosition="-1" position="0,0" size="865,623" alphatest="on" />
    <ePixmap pixmap="SF_HD/menu/ico_backup.png" position="32,41" size="40,40" alphatest="blend" transparent="1" />
    <widget source="Title" render="Label" position="90,50" size="600,32" font="Semiboldit;32" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1" />
    <ePixmap pixmap="SF_HD/icons/clock.png" position="750,55" zPosition="1" size="20,20" alphatest="blend" />
    <widget source="global.CurrentTime" render="Label" position="770,57" zPosition="1" size="50,20" font="Regular;20" foregroundColor="foreground" backgroundColor="#27d9dee2" halign="right" transparent="1">
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <ePixmap pixmap="SF_HD/border_sf.png" position="125,165" zPosition="-1" size="620,420" transparent="1" alphatest="blend" />
<widget source="key_red" render="Label" position="86,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<eLabel text="View" position="278,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<eLabel text="Remove All" position="473,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<eLabel text="Remove" position="653,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<ePixmap pixmap="SF_HD/buttons/red.png" position="45,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/green.png" position="240,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/blue.png" position="435,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/yellow.png" position="625,98" size="25,25" alphatest="blend" />
	<widget source="menu" render="Listbox" position="135,180" size="600,350" scrollbarMode="showNever" backgroundColor="#a7a7a7" foregroundColor="#2E2E2E" zPosition="1" transparent="1">
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

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.path = config.crashpath.value
		self.setTitle(_("View or Remove Crashlog files"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"ok": self.Ok,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.Ok,
			"yellow": self.YellowKey,
			"blue": self.BlueKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("View"))
		self["key_yellow"] = StaticText(_("Remove"))
		self["key_blue"] = StaticText(_("Remove All"))
		self.list = []
		self["menu"] = List(self.list)
		self.CfgMenu()
		
	def CfgMenu(self):
		self.list = []
		minipng = LoadPixmap(cached=True, path="/usr/share/enigma2/sfpanel/crashmini.png")
		if pathExists(self.path):
			crashfiles = os.listdir(self.path)
			for line in crashfiles:
				if "enigma2_crash" in line:
					try:
						self.list.append((line,"%s" % time.ctime(os.path.getctime(self.path + line)), minipng))
					except Exception as e:
						now = time.localtime(time.time())
						logging('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (now.tm_mday, now.tm_mon, now.tm_year, now.tm_hour, now.tm_min, now.tm_sec, str(e)))
		self.list.sort()
		self["menu"].setList(self.list)
		self["actions"] = ActionMap(["OkCancelActions"], { "cancel": self.close}, -1)
		
	def Ok(self):
		try:
			if self["menu"].getCurrent()[0] is not None:
				item = self.path + self["menu"].getCurrent()[0]
				self.session.openWithCallback(self.CfgMenu,LogScreen, item)
		except Exception as e:
			now = time.localtime(time.time())
			logging('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (now.tm_mday, now.tm_mon, now.tm_year, now.tm_hour, now.tm_min, now.tm_sec, str(e)))
	
	def YellowKey(self):
		if self["menu"].getCurrent()[0] is not None:
			item = self.path + self["menu"].getCurrent()[0]
			if fileExists(item):
				os.remove(item)
			self.mbox = self.session.open(MessageBox,(_("Removed %s") % item), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def BlueKey(self):
		log_name = []
		dirs = os.listdir(self.path)
		for log_file in dirs:
			if log_file.endswith(".log") and log_file.startswith("enigma2_crash"):
				log_name.append('%s%s' % (self.path, log_file))
		try:
			for file in log_name:
				os.remove(file)
		except Exception as e:
			now = time.localtime(time.time())
			logging('%02d:%02d:%d %02d:%02d:%02d - %s\r\n' % (now.tm_mday, now.tm_mon, now.tm_year, now.tm_hour, now.tm_min, now.tm_sec, str(e)))
		self.mbox = self.session.open(MessageBox,(_("Removed All Crashlog Files") ), MessageBox.TYPE_INFO, timeout = 4 )
		self.CfgMenu()
		
	def exit(self):
		self.close()
######################################################################################
class LogScreen(Screen):
	skin = """
<screen name="LogScreen" position="209,48" size="865,623" title="View Crashlog file" flags="wfNoBorder" backgroundColor="transparent">
	<ePixmap pixmap="SF_HD/Bg_EPG_view.png" zPosition="-1" position="0,0" size="865,623" alphatest="on" />
    <ePixmap pixmap="SF_HD/menu/ico_backup.png" position="32,41" size="40,40" alphatest="blend" transparent="1" />
    <widget source="Title" render="Label" position="90,50" size="600,32" font="Semiboldit;32" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1" />
    <ePixmap pixmap="SF_HD/icons/clock.png" position="750,55" zPosition="1" size="20,20" alphatest="blend" />
    <widget source="global.CurrentTime" render="Label" position="770,57" zPosition="1" size="50,20" font="Regular;20" foregroundColor="foreground" backgroundColor="#27d9dee2" halign="right" transparent="1">
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <widget source="key_red" render="Label" position="86,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<eLabel text="Restart GUI" position="278,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<eLabel text="Save" position="653,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<ePixmap pixmap="SF_HD/buttons/red.png" position="45,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/green.png" position="240,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/blue.png" position="435,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/yellow.png" position="625,98" size="25,25" alphatest="blend" />
	 <ePixmap pixmap="SF_HD/border_console.png" position="125,165" zPosition="-1" size="620,420" transparent="1" alphatest="blend" />
        <widget name="text" position="130,170" size="600,400" backgroundColor="black" foregroundColor="white" transparent="1" font="Console;14"/>
  </screen>"""

	def __init__(self, session, what):
		self.session = session
		Screen.__init__(self, session)
		self.iConsole = iConsole()
		self.crashfile = what
		self.setTitle(_("View Crashlog file"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"green": self.GreenKey,
			"yellow": self.YellowKey,
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Restart GUI"))
		self["key_yellow"] = StaticText(_("Save"))
		self["text"] = ScrollLabel("")
		self.listcrah()
		
	def exit(self):
		self.close()
	
	def GreenKey(self):
		self.session.open(TryQuitMainloop, 3)
		
	def YellowKey(self):
		self.iConsole.ePopen("gzip %s && mv %s.gz /tmp" % (self.crashfile, self.crashfile), self.info_create)
		
	def info_create(self, result, retval, extra_args):
		if retval is 0:
			self.mbox = self.session.open(MessageBox,_("%s.gz created in /tmp") % self.crashfile, MessageBox.TYPE_INFO, timeout = 4)
		else:
			self.mbox = self.session.open(MessageBox,_("Failure..."), MessageBox.TYPE_INFO, timeout = 4)
		
	def listcrah(self):
		list = ""
		with open(self.crashfile, "r") as files:
			for line in files:
				if "Traceback (most recent call last):" in line or "PC:" in line:
					for line in files:
						list += line
						if "]]>" in line:
							break
		self["text"].setText(list)
		self["actions"] = ActionMap(["OkCancelActions", "DirectionActions"], { "cancel": self.close, "up": self["text"].pageUp, "left": self["text"].pageUp, "down": self["text"].pageDown, "right": self["text"].pageDown,}, -1)

######################################################################################

SKIN_HD = """
<screen name="SFecminfo" position="265,140" size="750,425" title="Ecm Info" zPosition="1">
  <eLabel position="20,58" size="710,2" backgroundColor="grey" zPosition="4" />
  <eLabel position="20,91" size="710,2" backgroundColor="grey" zPosition="4" />
  <eLabel position="20,319" size="710,2" backgroundColor="grey" zPosition="4" />
  <eLabel position="20,353" size="710,2" backgroundColor="grey" zPosition="4" />
  <eLabel position="50,388" size="650,2" backgroundColor="grey" zPosition="4" />
  <widget source="boxinfo" render="Label" position="10,5" size="730,25" font="Regular; 23" zPosition="2" foregroundColor="foreground" transparent="1" valign="top" noWrap="1" halign="center" />
  <widget source="hardinfo" render="Label" position="10,30" size="730,25" font="Regular; 23" zPosition="2" foregroundColor="grey" transparent="1" valign="top" noWrap="1" halign="center" />
  <widget name="ecmfile" render="Label" position="11,98" size="730,215" font="Regular; 23" zPosition="2" foregroundColor="foreground" transparent="1" valign="top" noWrap="1" halign="center" />
  <widget source="emuname" render="Label" position="20,62" size="470,25" font="Regular; 22" zPosition="2" foregroundColor="unfec000" transparent="1" valign="top" halign="left" />
  <widget source="txtcaid" render="Label" position="430,62" size="300,25" font="Regular; 22" zPosition="2" foregroundColor="grey" transparent="1" valign="top" halign="right" />
  <widget source="caids" render="Label" position="6,325" size="740,25" font="Regular; 22" zPosition="2" foregroundColor="grey" transparent="1" valign="top" halign="center" />
  <widget source="pids" render="Label" position="5,359" size="740,25" font="Regular; 22" zPosition="2" foregroundColor="foreground" transparent="1" valign="top" halign="center" />
  <widget source="res" render="Label" position="14,395" size="180,25" font="Regular; 22" zPosition="2" foregroundColor="grey" transparent="1" valign="top" halign="right" />
<widget source="abit" render="Label" position="485,395" size="230,25" font="Regular; 22" zPosition="2" foregroundColor="grey" transparent="1" valign="top" halign="left" />
<widget source="vbit" render="Label" position="180,395" size="320,25" font="Regular; 22" zPosition="2" foregroundColor="grey" transparent="1" valign="top" halign="center" />
</screen>"""

class SFecminfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.skin = SKIN_HD
		self.setTitle(_("Ecm Info"))
		self.videoBitrate = self.audioBitrate = None
		self.resolution = self.audiocodec = self.videocodec = ''
		self.active_caid = 'FFFF'
		self.maincolor = self.convert_color('#00FFFFFF')
		self.emmcolor = self.convert_color('#0003a902')
		self.ecmcolor = self.convert_color('#00f0bf4f')
		self["ecmfile"] = ScrollLabel("")
		self["boxinfo"] = StaticText()
		self["hardinfo"] = StaticText()
		self["emuname"] = StaticText()
		self["txtcaid"] = StaticText()
		self["caids"] = StaticText()
		self["pids"] = StaticText()
		self["key_red"] = StaticText(_("Close"))
		self["res"] = StaticText()
		self["vbit"] = StaticText()
		self["abit"] = StaticText()
		self.TxtCaids = {
			"26" : "BiSS", "01" : "Seca Mediaguard", "06" : "Irdeto", "17" : "BetaCrypt", "05" : "Viacces", "18" : "Nagravision", "09" : "NDS-Videoguard",\
			"0B" : "Conax", "0D" : "Cryptoworks", "4A" : "DRE-Crypt", "27" : "ExSet", "0E" : "PowerVu", "22" : "Codicrypt", "07" : "DigiCipher",\
			"56" : "Verimatrix", "7B" : "DRE-Crypt", "A1" : "Rosscrypt"}
		self["ecmfile"].setText(self.ecm_view())
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions"],
		{
                        "red": self.close,
			"back": self.close,
			"ok": self.close,
			"right": self.close,
			"left": self.close,
			"down": self.close,
			"up": self.close,
		}, -2)
		ref = session.nav.getCurrentlyPlayingServiceReference()
		vpid = apid = dvbnamespace = tsid = onid = -1
		service = session.nav.getCurrentService()
		if service:
			serviceInfo = service.info()
			info = service and service.info()
			vpid = info.getInfo(iServiceInformation.sVideoPID)
			apid = info.getInfo(iServiceInformation.sAudioPID)
			tsid = info.getInfo(iServiceInformation.sTSID)
			onid = info.getInfo(iServiceInformation.sONID)
			dvbnamespace = info.getInfo(iServiceInformation.sNamespace)
			self.resolution = self.resolutioninfo(serviceInfo)
			audio = service.audioTracks()
			if audio:
				if audio.getCurrentTrack() > -1:
					self.audiocodec = str(audio.getTrackInfo(audio.getCurrentTrack()).getDescription()).replace(",","")
			self.videocodec = ("MPEG2", "MPEG4", "MPEG1", "MPEG4-II", "VC1", "VC1-SM", "")[info.getInfo(iServiceInformation.sVideoType)]
		if apid and binary_file:
			self.audioBitrate = eBitrateCalculator(apid, dvbnamespace, tsid, onid, 1000, 64*1024)
			self.audioBitrate.callback.append(self.getAudioBitrateData)
		if vpid and binary_file:
			self.videoBitrate = eBitrateCalculator(vpid, dvbnamespace, tsid, onid, 1000, 1024*1024)
			self.videoBitrate.callback.append(self.getVideoBitrateData)
		self.Timer = eTimer()
		self.Timer.callback.append(self.ecmfileinfo)
		self.Timer.start(1000*2, False)
		self.onShow.append(self.staticinfo)

	def getVideoBitrateData(self,value, status): 
		if status:
			self["vbit"].text = 'VIDEO %s: %d Kb/s' % (self.videocodec, value)
			self["res"].text = self.resolution
		else:
			self.videoBitrate = None

	def getAudioBitrateData(self,value, status): 
		if status:
			self["abit"].text = 'AUDIO %s: %s Kb/s' % (self.audiocodec, value)
		else:
			self.audioBitrate = None

	def ecmfileinfo(self):
		self["ecmfile"].setText(self.ecm_view())

	def staticinfo(self):
		self["boxinfo"].text = self.boxinfo()
		self["emuname"].text = self.emuname()
		self["hardinfo"].text = self.hardinfo()
		self["pids"].text = self.pidsline()
		self["caids"].text = self.caidline()
		
	def convert_color(self, color_in):
		hex_color = {'0':'0', '1':'1', '2':'2', '3':'3', '4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9',\
			'a':':', 'b':';', 'c':'<', 'd':'=', 'e':'>', 'f':'?', 'A':':', 'B':';', 'C':'<', 'D':'=', 'E':'>', 'F':'?'}
		color_out = '\c'
		for i in range(1, len(color_in)):
			color_out += hex_color.get(color_in[i])
		return color_out

	def caidline(self):
		array_caid = []
		bar_caids = ecm_caid = ''
		service = self.session.nav.getCurrentService()
		if service:
			info = service and service.info()
			caid_default = ['01XX', '05XX', '06XX', '09XX', '0BXX', '0DXX', '17XX', '18XX', '26XX', '27XX', '4AXX', '56XX']
			caidinfo = self.getServiceInfoString(info, iServiceInformation.sCAIDs)
			if caidinfo:
				ecm_caid = self.active_caid
				for caid in caidinfo.split():
					array_caid.append(caid.strip())
				caidinfo = ' '.join(str(x) for x in set(array_caid))
				bar_caids = self.maincolor + ''
				array_caid = caidinfo.split()
				for i in range(len(caid_default)):
					for j in range(len(caidinfo.split())):
						if caid_default[i][:2] == array_caid[j][:2]:
							if caid_default[i][:2] == ecm_caid[:2]:
								caid_default[i] = self.ecmcolor + ecm_caid + self.maincolor
							else:
								caid_default[i] = self.emmcolor + array_caid[j] + self.maincolor
					bar_caids += caid_default[i] + '  '
			else:
				for i in range(len(caid_default)):
					bar_caids += self.maincolor + caid_default[i] + '  '
			return bar_caids.strip()

	def pidsline(self):
		vpid = apid = tsid = onid = sid = -1
		service = self.session.nav.getCurrentService()
		if service is not None:
			info = service and service.info()
			sid = info.getInfo(iServiceInformation.sSID)
			vpid = info.getInfo(iServiceInformation.sVideoPID)
			apid = info.getInfo(iServiceInformation.sAudioPID)
			tsid = info.getInfo(iServiceInformation.sTSID)
			onid = info.getInfo(iServiceInformation.sONID)
		return 'SID: %0.4X  VPID: %0.4X  APID: %0.4X  TSID: %0.4X ONID: %0.4X' % (sid, vpid, apid, tsid, onid)

	def resolutioninfo(self, serviceInfo):
		xres = serviceInfo.getInfo(iServiceInformation.sVideoWidth)
		if xres == -1:
			return ''
		yres = serviceInfo.getInfo(iServiceInformation.sVideoHeight)
		mode = ('i', 'p', ' ')[serviceInfo.getInfo(iServiceInformation.sProgressive)]
		fps  = str((serviceInfo.getInfo(iServiceInformation.sFrameRate) + 500) / 1000)
		return str(xres) + 'x' + str(yres) + mode + '(%s)' % fps

	def getServiceInfoString(self, info, what):
		value = info.getInfo(what)
		if value == -3:
			line_caids = info.getInfoObject(what)
			if line_caids and len(line_caids) > 0:
				return_value = ''
				for caid in line_caids:
					return_value += '%.4X ' % caid
				return return_value[:-1]
			else:
				return ''
		return '%d' % value

	def ecm_view(self):
		service = self.session.nav.getCurrentService()
		if service is not None:
			info = service and service.info()
			list = caidvalue = ''
			port_flag = 0
			zero_line = '0000'
			self["txtcaid"].text = ''
			iscrypt = info.getInfo(iServiceInformation.sIsCrypted)
			if not iscrypt or iscrypt == -1:
				self["txtcaid"].text = _('Free-to-air')
			elif iscrypt and not os.path.isfile('/tmp/ecm.info'):
				self["txtcaid"].text = _('No parse cannot emu')
			elif iscrypt and os.path.isfile('/tmp/ecm.info'):
				try:
					if not os.stat('/tmp/ecm.info').st_size:
						self["txtcaid"].text = _('No parse cannot emu')
				except:
					self["txtcaid"].text = _('No parse cannot emu')
			if os.path.isfile("/tmp/ecm.info"):
				try:
					ecmfiles = open('/tmp/ecm.info').readlines()
				except:
					pass
				if ecmfiles:
					for line in ecmfiles:
						if 'port:' in line: 
							port_flag  = 1
						if 'caid:' in line or 'provider:' in line or 'provid:' in line or 'pid:' in line or 'hops:' in line or 'system:' in line or 'address:' in line or 'using:' in line or 'ecm time:' in line:
							line = line.replace(' ','').replace(':',': ')
						if 'from:' in line or 'protocol:' in line or 'caid:' in line or 'pid:' in line or 'reader:' in line or 'hops:' in line or 'system:' in line or 'Service:' in line or 'CAID:' in line or 'Provider:' in line:
							line = line.strip('\n') + '  '
						if 'Signature' in line:
							line = ""
						if '=' in line:
							line = line.lstrip('=').replace('======', "").replace('\n', "").rstrip() + ', '
						if 'ecmtime:' in line:
							line = line.replace('ecmtime:', 'ecm time:')
						if 'response time:' in line:
							line = line.replace('response time:', 'ecm time:').replace('decoded by', 'by')
						if not line.startswith('\n'): 
							if 'protocol:' in line and port_flag == 0:
								line = '\n' + line
							if 'pkey:' in line:
								line = '\n' + line + '\n'
							list += line
						if "caid:" in line:
							caidvalue = line.strip("\n").split()[-1][2:]
							if len(caidvalue) < 4:
								caidvalue = zero_line[len(caidvalue):] + caidvalue
						elif "CaID" in line or "CAID" in line:
							caidvalue = line.split(',')[0].split()[-1][2:]
					self["txtcaid"].text = self.TxtCaids.get(caidvalue[:2].upper(), ' ')
					self.active_caid = caidvalue.upper()
					return list
		return ''
		
	def emuname(self):
		camd = ""
                serlist = None
                camdlist = None
                nameemu = []
                nameser = []
                # Alternative SoftCam Manager 
		if os.path.isfile("/usr/lib/enigma2/python/Plugins/Extensions/AlternativeSoftCamManager/plugin.py"): 
			if config.plugins.AltSoftcam.actcam.value != "none": 
				return config.plugins.AltSoftcam.actcam.value 
			else: 
				return None
		#egami
		elif os.path.isfile("/tmp/egami.inf"):
			for line in open("/tmp/egami.inf"):
				if 'Current emulator:' in line:
					return line.split(':')[-1].lstrip().strip('\n')
		#Pli
		elif os.path.isfile("/etc/init.d/softcam") or os.path.isfile("/etc/init.d/cardserver"):
			if os.path.isfile("/etc/init.d/softcam"):
				for line in open("/etc/init.d/softcam"):
					if "echo" in line:
						nameemu.append(line)
				if len(nameemu) > 1:
					camdlist = "%s" % nameemu[1].split('"')[1]
			if os.path.isfile("/etc/init.d/cardserver"):
				for line in open("/etc/init.d/cardserver"):
					if "echo" in line:
						nameser.append(line)
				if len(nameser) > 1:
					serlist = "%s" % nameser[1].split('"')[1]
			if serlist is not None and camdlist is not None:
				return ("%s %s" % (serlist, camdlist))
			elif camdlist is not None:
				return "%s" % camdlist
			elif serlist is not None:
				return "%s" % serlist
			return ""
		else:
			emu = ""
			ecminfo = "%s %s" % (cardserver.split('\n')[0], emu.split('\n')[0])
		return ecminfo

	def status(self):
		status = ''
		if os.path.isfile("/usr/lib/opkg/status"):
			status = "/usr/lib/opkg/status"
		elif os.path.isfile("/usr/lib/ipkg/status"):
			status = "/usr/lib/ipkg/status"
		elif os.path.isfile("/var/lib/opkg/status"):
			status = "/var/lib/opkg/status"
		elif os.path.isfile("/var/opkg/status"):
			status = "/var/opkg/status"
		return status

	def boxinfo(self):
		box = software = enigma = driver = tmp_line = ''
		package = 0
		try:
			if os.path.isfile(self.status()):
				for line in open(self.status()):
					if "-dvb-modules" in line and "Package:" in line:
						package = 1
					elif "driver" in line and "Package:" in line:
						package = 1
					elif "kernel-module-player2" in line and "Package:" in line:
						package = 1
					if "Version:" in line and package == 1:
						package = 0
						tmp_line = line.split()[-1].split('+')[-1].split('-')[0]
						driver = '%s.%s.%s' %(tmp_line[6:], tmp_line[4:-2], tmp_line[:4])
						break
			if os.path.isfile("/proc/version"):
				enigma = open("/proc/version").read().split()[2]
			if os.path.isfile("/proc/stb/info/boxtype"):
				box = open("/proc/stb/info/boxtype").read().strip().upper()
			elif os.path.isfile("/proc/stb/info/vumodel"):
				box = "Vu+ " + open("/proc/stb/info/vumodel").read().strip().capitalize()
			elif os.path.isfile("/proc/stb/info/model"):
				box = open("/proc/stb/info/model").read().strip().upper()
			if os.path.isfile("/etc/issue"):
				if os.path.isfile("/etc/issue"):
					for line in open("/etc/issue"):
						if not line.startswith('Welcom') and '\l' in line:
							software += line.capitalize().replace('\n', '').replace('\l', '').replace('\\', '').strip()[:-1]
				else:
					software = _("undefined")
				software = ' (%s)' % software.strip()
			if os.path.isfile("/etc/vtiversion.info"):
				software = ''
				for line in open("/etc/vtiversion.info"):
					software += line.split()[0].split('-')[0] + ' ' + line.split()[-1].replace('\n', '')
				software = ' (%s)' % software.strip()
			return _('%s%s  Kernel: %s (%s)') % (box, software, enigma, driver)
		except:
			pass
		return ''

	def hardinfo(self):
		if os.path.isfile("/proc/cpuinfo"):
			cpu_count = 0
			processor = cpu_speed = cpu_family = cpu_variant = temp = ''
			core = _("core")
			cores = _("cores")
			for line in open('/proc/cpuinfo'):
				if "system type" in line:
					processor = line.split(':')[-1].split()[0].strip().strip('\n')
				elif "cpu MHz" in line:
					cpu_speed =  line.split(':')[-1].strip().strip('\n')
					cpu_count += 1
				elif "cpu type" in line:
					processor = line.split(':')[-1].strip().strip('\n')
				elif "cpu family" in line:
					cpu_family = line.split(':')[-1].strip().strip('\n')
				elif "cpu variant" in line:
					cpu_variant = line.split(':')[-1].strip().strip('\n')
			if os.path.isfile("/proc/stb/sensors/temp0/value") and os.path.isfile("/proc/stb/sensors/temp0/unit"):
				temp = "%s%s%s" % (open("/proc/stb/sensors/temp0/value").read().strip('\n'), unichr(176).encode("latin-1"), open("/proc/stb/sensors/temp0/unit").read().strip('\n'))
			elif os.path.isfile("/proc/stb/fp/temp_sensor_avs"):
				temp = "%s%sC" % (open("/proc/stb/fp/temp_sensor_avs").read().strip('\n'), unichr(176).encode("latin-1"))
			if cpu_variant is '':
				return _("%s, %s Mhz (%d %s) %s") % (processor, cpu_speed, cpu_count, cpu_count > 1 and cores or core, temp)
			else:
				return "%s(%s), %s %s" % (processor, cpu_family, cpu_variant, temp)
		else:
			return _("undefined")

###############################################
class Preview(Pixmap):
	def __init__(self):
		Pixmap.__init__(self)
                self.picload = ePicLoad()
		self.picload.PictureData.get().append(self.paintIconPixmapCB)
                              
	def onShow(self):
		Pixmap.onShow(self)
		self.picload.setPara((self.instance.size().width(), self.instance.size().height(), 1, 1, False, 1, "#00000000"))
                                                    
	def paintIconPixmapCB(self, picInfo=None):
		ptr = self.picload.getData()
		if ptr != None:
			self.instance.setPixmap(ptr.__deref__())
                                                                                      
	def updateIcon(self, filename):
		self.picload.startDecode(filename)

class skinpart(Screen):
	skin = """

<screen name="skinpart" position="209,48" size="865,623" flags="wfNoBorder" backgroundColor="transparent" title="SkinPart install">
<ePixmap pixmap="SF_HD/Bg_EPG_view.png" zPosition="-1" position="0,0" size="865,623" alphatest="on"/>
    <ePixmap pixmap="SF_HD/menu/ico_title_Setup.png" position="26,41" size="40,40" alphatest="blend" transparent="1"/>
    <ePixmap pixmap="SF_HD/icons/clock.png" position="750,55" zPosition="1" size="20,20" alphatest="blend"/>
    <widget source="global.CurrentTime" render="Label" position="770,57" zPosition="1" size="50,20" font="Regular;20" foregroundColor="#1c1c1c" halign="right" backgroundColor="#27d9dee2" transparent="1">
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <widget source="Title" render="Label" position="90,50" size="600,32" font="Semiboldit;32" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1" />
     <widget name="preview" position="520,250" size="280,210" zPosition="3" alphatest="blend" transparent="1" borderWidth="2" borderColor="white" /> 
    <ePixmap pixmap="SF_HD/buttons/red.png" position="45,98" size="25,25" alphatest="blend"/>
    <ePixmap pixmap="SF_HD/buttons/green.png" position="240,98" size="25,25" alphatest="blend" />
    <widget source="key_red" render="Label" position="83,98" zPosition="2" size="150,25" foregroundColor="#1c1c1c" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" transparent="1"/>
   <widget source="key_blue" render="Label" position="473,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
   <ePixmap pixmap="SF_HD/buttons/blue.png" position="435,98" size="25,25" alphatest="blend" />
    <widget source="key_green" render="Label" position="278,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget source="menu" render="Listbox" position="60,170" size="420,340" scrollbarMode="showNever" backgroundColor="#27d9dee2" transparent="1">
	<convert type="TemplatedMultiContent">
		{"template": [
			MultiContentEntryText(pos = (10, 2), size = (630, 25), font=0, flags = RT_HALIGN_LEFT, text = 0), # index 2 is the Menu Titel
										],
	"fonts": [gFont("Regular", 23)],
	"itemHeight": 30
	}
	</convert>
	</widget>
	
    
   </screen>"""
	  
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session
		self.list = []
		self.image="first"
		self["menu"] = List(self.list)
		self["preview"] = Preview()
		self.feedlist()
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("Install"))
		self["key_blue"] = StaticText(_("Remove"))
		self.ctimer = eTimer()
		self.ctimer.callback.append(self.__run)
		self.ctimer.start(1000,0)
		                                                
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "DirectionActions"],
			{
				"cancel": self.cancel,
				"ok": self.ok,
				"green": self.setup,
				"blue": self.remove,
				"red": self.cancel,
				"up": self.Kup,
				"down": self.Kdown,
				"left": self.Kleft,
				"right": self.Kright,
			},-1)

        def __run(self):
        	if len(self.list)==0:
        		image=""
        	elif self.image=="first":
			self.Kup()
        	elif self.image!="":
			self.__updateimage()
		
	def __updateimage(self):
		img="/tmp/.lbimg%s" % (self.image)
		eimg="/tmp/.lbimg%s.error" % (self.image)
		print ("Check image: %s" % img)
		if fileExists(img) and os.path.getsize(img)>0:
			self["preview"].updateIcon(img)
			self["preview"].show()
			self.image=""
		elif fileExists(eimg) :
			print "Error downloading %s" % img
			os.remove(eimg)	
			self["preview"].updateIcon("/usr/share/enigma2/SF_HD/sfmenu/noimage.png")
			self["preview"].show()
			self.image=""
		else:
			print "Preview - wait for finish download"
				
	def feedlist(self):
		self.list = []
		camdlist = os.popen("opkg list | grep skinpartsf")
		for line in camdlist.readlines():
			try:
				self.list.append(("%s %s" % (line.split(' - ')[0], line.split(' - ')[1]), line.split(' - ')[-1]))
			except:
				pass
		camdlist.close()
		self["menu"].setList(self.list)
	
	def Kup(self):
		if len(self.list)!=0:
			self["menu"].selectPrevious()
			self.imageDown()		
		
	def Kdown(self):
		if len(self.list)!=0:
			self["menu"].selectNext()
			self.imageDown()
	def Kleft(self):
		if len(self.list)!=0:
			self["menu"].selectPrevious()
			self.imageDown()
	def Kright(self):
		if len(self.list)!=0:
			self["menu"].selectNext()
			self.imageDown()
	
        def runDownloadImg(self, img):
		try:
			index=self["menu"].getIndex()
		except:
			index=0
        	img=self["menu"].getCurrent()[0]
		oimg="http://feeds.soldiersat.eu/capturas/preview/%s.png" % (img)
                timg="/tmp/%s.tmp" % img
                dimg="/tmp/.lbimg%s" % img
                print ("Downloading image  %s to %s") % (oimg, dimg)
                if not fileExists(dimg):
                	try:
                		req = urllib2.Request(oimg)
				u = urllib2.urlopen(req)
				fdest = open(timg, 'wb')
				while True:
					data = u.read(8192) 
					if not data: break
					fdest.write(data)
				fdest.flush()
				fdest.close()
				os.rename(timg, dimg)
				print ("Done download img  %s") % oimg
				
			except: 
				print "Error downloading %s" % oimg
				open("%s.error" % (dimg), 'a').close()
		#run download img cache	
		for x in range(0, self["menu"].count()):
			img=self.list[x][0]
			dimg="/tmp/.lbimg%s" % img
			if ( x==index-1) or  (x==index+1 ) or (x==index):
				if not fileExists(dimg):
					oimg="http://feeds.soldiersat.eu/capturas/preview/%s.png" % (img)
					timg="/tmp/%s.tmp" % img
					print "Downloading %s" % (oimg)
					try:
						req = urllib2.Request(oimg)
						u = urllib2.urlopen(req)
						fdest = open(timg, 'wb')
						while True:
							data = u.read(8192)
							if not data: break
							fdest.write(data)
						fdest.flush()
						fdest.close()
						os.rename(timg, dimg)
						print ("Done download cache img  %s") % oimg
				        except:
				        	print "Error downloading %s" % oimg
				        	open("%s.error" % (dimg), 'a').close()        
			else:
				if fileExists(dimg):
					os.remove(dimg)
			
                        
	def imageDown(self):
		self.image=self["menu"].getCurrent()[0]
		process = threading.Thread(target=self.runDownloadImg, args=[self.image])
		process.setDaemon(True)
		process.start()
				
	def ok(self):
		self.setup()
		
	def setup(self):
		os.system("opkg install --force-overwrite %s" % self["menu"].getCurrent()[0])
                self.session.openWithCallback(self.restartGUI,MessageBox,_("GUI needs a restart to apply a new skinpart sfteam\nDo you want to restart the GUI now?"), MessageBox.TYPE_YESNO)

		
	def remove(self):
                self.session.openWithCallback(self.remove2,MessageBox,_("Se va a borrar la skinpart, estas seguro?? recuerda tras borrarla instalar otra skinpart del mismo modelo a la borrada"), MessageBox.TYPE_YESNO)

	def remove2(self, answer):
		if answer is True:
			os.system("opkg remove %s" % self["menu"].getCurrent()[0])
			self.mbox = self.session.open(MessageBox,_("skinpart is delete"), MessageBox.TYPE_INFO, timeout = 10 )

	def restartGUI(self, answer):
		if answer is True:
			self.session.open(TryQuitMainloop, 3)
		
			
	def cancel(self):
		os.system('rm -f /tmp/.lbimg*')
		self.ctimer.stop()
		self.close()
####################################
##############################################################################
class memoryinfo(Screen):
	skin = """
<screen name="memoryinfo" position="209,48" size="865,623" title="Clear Memory" flags="wfNoBorder" backgroundColor="transparent">
	    <ePixmap pixmap="SF_HD/Bg_EPG_view.png" zPosition="-1" position="0,0" size="865,623" alphatest="on" />
    <ePixmap pixmap="SF_HD/menu/ico_backup.png" position="32,41" size="40,40" alphatest="blend" transparent="1" />
    <widget source="Title" render="Label" position="90,50" size="600,32" font="Semiboldit;32" foregroundColor="#5d5d5d" backgroundColor="#27b5b9bd" transparent="1" />
    <ePixmap pixmap="SF_HD/icons/clock.png" position="750,55" zPosition="1" size="20,20" alphatest="blend" />
    <widget source="global.CurrentTime" render="Label" position="770,57" zPosition="1" size="50,20" font="Regular;20" foregroundColor="foreground" backgroundColor="#27d9dee2" halign="right" transparent="1">
      <convert type="ClockToText">Format:%H:%M</convert>
    </widget>
    <ePixmap pixmap="SF_HD/border_sf.png" position="125,165" zPosition="-1" size="620,420" transparent="1" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/red.png" position="45,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/green.png" position="240,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/yellow.png" position="435,98" size="25,25" alphatest="blend" />
    <ePixmap pixmap="SF_HD/buttons/blue.png" position="625,98" size="25,25" alphatest="blend" />
  <widget source="key_yellow" render="Label" position="473,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget source="key_blue" render="Label" position="653,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget source="key_green" render="Label" position="278,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
    <widget source="key_red" render="Label" position="86,101" zPosition="1" size="150,25" font="Regular;20" halign="center" valign="center" backgroundColor="darkgrey" foregroundColor="foreground" transparent="1" />
<widget source="MemoryLabel" render="Label" position="161,200" size="150,22" font="Regular; 26" halign="right" foregroundColor="black" backgroundColor="#a7a7a7" valign="center" transparent="1" />
<widget source="root" render="Label" position="105,590" size="600,22" zPosition="3" font="Regular; 20" halign="right" foregroundColor="#5d5d5d" backgroundColor="#a7a7a7" valign="center" transparent="1" />
	<widget source="memTotal" render="Label" position="161,242" zPosition="2" size="450,22" font="Regular;20" halign="left" valign="center" backgroundColor="#a7a7a7" foregroundColor="blue" transparent="1" />
	<widget source="bufCache" render="Label" position="161,269" zPosition="2" size="450,22" font="Regular;20" halign="left" valign="center" backgroundColor="#a7a7a7" foregroundColor="white" transparent="1" />
<ePixmap pixmap="SF_HD/liberar_ram.png" zPosition="-1" position="300,290" size="300,300" alphatest="on" />
   </screen>"""

	def __init__(self, session):
		self.session = session
		Screen.__init__(self, session)
		self["memTotal"] = StaticText()
		self["bufCache"] = StaticText()
		self["MemoryLabel"] = StaticText(_("Memory:"))
		self["root"] = StaticText(_("Pulse tecla UP para crear root en caso no existir archivo en crontabs"))
		self["shortcuts"] = ActionMap(["ShortcutActions", "WizardActions", "DirectionActions"],
		{
			"green": self.clear,
			"blue": self.cron,
			"yellow": self.removecron,
			"cancel": self.exit,
			"back": self.exit,
			"red": self.exit,
			"ok": self.exit,
			"up": self.crearroot,
			
			})
		self["key_red"] = StaticText(_("Close"))
		self["key_green"] = StaticText(_("free memory"))
		self["key_blue"] = StaticText(_("add cron"))
		self["key_yellow"] = StaticText(_("remove cron"))
                self.onShow.append(self.Title)


	def Title(self):
		self.setTitle(_("Clear Memory"))
		self.infomem()

	def crearroot(self):
		if fileExists('/etc/cron/crontabs/root'):
			self.mbox = self.session.open(MessageBox,(_("ya existe archivo root")), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			os.system("touch /var/spool/cron/crontabs/root")
			self.mbox = self.session.open(MessageBox,(_("create archivo root")), MessageBox.TYPE_INFO, timeout = 4 )
	
	def clear(self):
		os.system("sync ; echo 3 > /proc/sys/vm/drop_caches")
		self.mbox = self.session.open(MessageBox,(_("memoria liberada")), MessageBox.TYPE_INFO, timeout = 4 )
		self.infomem()

	def cron(self):
		if fileExists('/etc/cron/crontabs/root'):
			os.system("sed -i '/drop_caches/d' /etc/cron/crontabs/root")
			os.system("echo '0 0-23/2 * * * sync; echo 3 > /proc/sys/vm/drop_caches' >> /etc/cron/crontabs/root")
			self.mbox = self.session.open(MessageBox,(_(" Add drop_caches for cron")), MessageBox.TYPE_INFO, timeout = 4 )
		else:
			self.mbox = self.session.open(MessageBox,(_(" No existe archivo root en /etc/crontabs")), MessageBox.TYPE_INFO, timeout = 4 )
			
	def removecron(self):
		os.system("sed -i '/drop_caches/d' /etc/cron/crontabs/root")	
		self.mbox = self.session.open(MessageBox,(_("Remove drop_caches for cron ")), MessageBox.TYPE_INFO, timeout = 4 )

	def infomem(self):
		memtotal = memfree = buffers = cached = ''
		persent = 0
		if fileExists('/proc/meminfo'):
			for line in open('/proc/meminfo'):
				if 'MemTotal:' in line:
					memtotal = line.split()[1]
				elif 'MemFree:' in line:
					memfree = line.split()[1]
				elif 'Buffers:' in line:
					buffers = line.split()[1]
				elif 'Cached:' in line:
					cached = line.split()[1]
			if '' is not memtotal and '' is not memfree:
				persent = int(memfree) / (int(memtotal) / 100)
			self["memTotal"].text = _("Total: %s Kb  Free: %s Kb (%s %%)") % (memtotal, memfree, persent)
			self["bufCache"].text = _("Buffers: %s Kb  Cached: %s Kb") % (buffers, cached)

		
	def exit(self):
		self.close()


		
	


