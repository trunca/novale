from Screen import Screen
from Components.config import config
from Components.ActionMap import ActionMap
from Components.Sources.StaticText import StaticText
from Components.Harddisk import harddiskmanager
from Components.NimManager import nimmanager
from Components.About import about
from Components.ScrollLabel import ScrollLabel
from Components.Button import Button
from Components.Pixmap import Pixmap, MultiPixmap

from Components.Label import Label
from Components.ProgressBar import ProgressBar

from Tools.StbHardware import getFPVersion
from enigma import eTimer, eLabel

from Components.HTMLComponent import HTMLComponent
from Components.GUIComponent import GUIComponent
import skin
from os import system, remove
from Tools.Directories import pathExists, fileExists, resolveFilename, SCOPE_PLUGINS, SCOPE_CURRENT_PLUGIN, SCOPE_CURRENT_SKIN, SCOPE_METADIR

class About(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		hddsplit, = skin.parameters.get("AboutHddSplit", (0,))

		AboutText = _("Hardware: ") + about.getHardwareTypeString() + "\n"
		AboutText += _("CPU: ") + about.getCPUInfoString() + "\n"
		AboutText += _("Image: ") + about.getImageTypeString() + "\n"
		AboutText += _("Installed: ") + about.getFlashDateString() + "\n"
		AboutText += _("Kernel version: ") + about.getKernelVersionString() + "\n"

		EnigmaVersion = "Enigma: " + about.getEnigmaVersionString()
		self["EnigmaVersion"] = StaticText(EnigmaVersion)
		AboutText += EnigmaVersion + "\n"
		AboutText += _("Enigma (re)starts: %d\n") % config.misc.startCounter.value

		GStreamerVersion = "GStreamer: " + about.getGStreamerVersionString().replace("GStreamer","")
		self["GStreamerVersion"] = StaticText(GStreamerVersion)
		AboutText += GStreamerVersion + "\n"

		ImageVersion = _("Last upgrade: ") + about.getImageVersionString()
		self["ImageVersion"] = StaticText(ImageVersion)
		AboutText += ImageVersion + "\n"

		AboutText += _("DVB drivers: ") + about.getDriverInstalledDate() + "\n"

		AboutText += _("Python version: ") + about.getPythonVersionString() + "\n"

		fp_version = getFPVersion()
		if fp_version is None:
			fp_version = ""
		else:
			fp_version = _("Frontprocessor version: %d") % fp_version
			AboutText += fp_version + "\n"

		self["FPVersion"] = StaticText(fp_version)

		self["TunerHeader"] = StaticText(_("Detected NIMs:"))
		AboutText += "\n" + _("Detected NIMs:") + "\n"

		nims = nimmanager.nimList()
		for count in range(len(nims)):
			if count < 4:
				self["Tuner" + str(count)] = StaticText(nims[count])
			else:
				self["Tuner" + str(count)] = StaticText("")
			AboutText += nims[count] + "\n"

		self["HDDHeader"] = StaticText(_("Detected HDD:"))
		AboutText += "\n" + _("Detected HDD:") + "\n"

		hddlist = harddiskmanager.HDDList()
		hddinfo = ""
		if hddlist:
			formatstring = hddsplit and "%s:%s, %.1f %sB %s" or "%s\n(%s, %.1f %sB %s)"
			for count in range(len(hddlist)):
				if hddinfo:
					hddinfo += "\n"
				hdd = hddlist[count][1]
				if int(hdd.free()) > 1024:
					hddinfo += formatstring % (hdd.model(), hdd.capacity(), hdd.free()/1024, "G", _("free"))
				else:
					hddinfo += formatstring % (hdd.model(), hdd.capacity(), hdd.free()/1024, "M", _("free"))
		else:
			hddinfo = _("none")
		self["hddA"] = StaticText(hddinfo)
		AboutText += hddinfo
		self["AboutScrollLabel"] = ScrollLabel(AboutText)
		self["key_blue"] = Button(_("System Info"))
		self["key_green"] = Button(_("Translations"))
		self["key_red"] = Button(_("Latest Commits"))
		
		self["actions"] = ActionMap(["ColorActions", "SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"red": self.showCommits,
				"green": self.showTranslationInfo,
				"blue": self.showsysteminfo,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown
			})

	def showTranslationInfo(self):
		self.session.open(TranslationInfo)

	def showsysteminfo(self):
		self.session.open(SFinfo)

	def showCommits(self):
		self.session.open(CommitInfo)


class TranslationInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		# don't remove the string out of the _(), or it can't be "translated" anymore.

		# TRANSLATORS: Add here whatever should be shown in the "translator" about screen, up to 6 lines (use \n for newline)
		info = _("TRANSLATOR_INFO")

		if info == "TRANSLATOR_INFO":
			info = "(N/A)"

		infolines = _("").split("\n")
		infomap = {}
		for x in infolines:
			l = x.split(': ')
			if len(l) != 2:
				continue
			(type, value) = l
			infomap[type] = value
		print infomap

		self["key_red"] = Button(_("Cancel"))
		self["TranslationInfo"] = StaticText(info)

		translator_name = infomap.get("Language-Team", "none")
		if translator_name == "none":
			translator_name = infomap.get("Last-Translator", "")

		self["TranslatorName"] = StaticText(translator_name)

		self["actions"] = ActionMap(["SetupActions"],
			{
				"cancel": self.close,
				"ok": self.close,
			})

class CommitInfo(Screen):
	def __init__(self, session):
		Screen.__init__(self, session)
		self.skinName = ["CommitInfo", "About"]
		self["AboutScrollLabel"] = ScrollLabel(_("Please wait"))

		self["actions"] = ActionMap(["SetupActions", "DirectionActions"],
			{
				"cancel": self.close,
				"ok": self.close,
				"up": self["AboutScrollLabel"].pageUp,
				"down": self["AboutScrollLabel"].pageDown,
				"left": self.left,
				"right": self.right
			})

		self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_(""))

		self.project = 0
		self.projects = [
			("enigma2", "Enigma2"),
			("openpli-oe-core", "Openpli Oe Core"),
			("enigma2-plugins", "Enigma2 Plugins"),
			("aio-grab", "Aio Grab"),
			("gst-plugin-dvbmediasink", "Gst Plugin Dvbmediasink"),
			("openembedded", "Openembedded"),
			("plugin-xmltvimport", "Plugin Xmltvimport"),
			("plugins-enigma2", "Plugins Enigma2"),
			("skin-magic", "Skin Magic"),
			("tuxtxt", "Tuxtxt")
		]
		self.cachedProjects = {}
		self.Timer = eTimer()
		self.Timer.callback.append(self.readCommitLogs)
		self.Timer.start(50, True)

	def readCommitLogs(self):
		url = 'http://sourceforge.net/p/openpli/%s/feed' % self.projects[self.project][0]
		commitlog = ""
		from urllib2 import urlopen
		try:
			commitlog += 80 * '-' + '\n'
			commitlog += url.split('/')[-2] + '\n'
			commitlog += 80 * '-' + '\n'
			for x in  urlopen(url, timeout=5).read().split('<title>')[2:]:
				for y in x.split("><"):
					if '</title' in y:
						title = y[:-7]
					if '</dc:creator' in y:
						creator = y.split('>')[1].split('<')[0]
					if '</pubDate' in y:
						date = y.split('>')[1].split('<')[0][:-6]
				commitlog += date + ' ' + creator + '\n' + title + 2 * '\n'
			self.cachedProjects[self.projects[self.project][1]] = commitlog
		except:
			commitlog = _("Currently the commit log cannot be retrieved - please try later again")
		self["AboutScrollLabel"].setText(commitlog)

        def updateCommitLogs(self):
		if self.cachedProjects.has_key(self.projects[self.project][1]):
			self["AboutScrollLabel"].setText(self.cachedProjects[self.projects[self.project][1]])
		else:
			self["AboutScrollLabel"].setText(_("Please wait"))
			self.Timer.start(50, True)

	def left(self):
		self.project = self.project == 0 and len(self.projects) - 1 or self.project - 1
		self.updateCommitLogs()

	def right(self):
		self.project = self.project != len(self.projects) - 1 and self.project + 1 or 0
		self.updateCommitLogs()

class SFinfo(Screen):
    skin = """
        <screen position="250,100" size="650,550" title="System Info">
          <eLabel backgroundColor="blue" position="100,120" size="500,2" zPosition="2" />	
          <eLabel font="Regular;29" position="150,80" size="435,38" text="System Info" transparent="1" zPosition="2" />	
          <ePixmap alphatest="blend" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/dev_flash.png" position="155,157" size="60,60" />
          <widget source="session.Event_Now" render="Progress" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/device.png" position="230,165" size="100,15" transparent="1" borderWidth="1" borderColor="grey" zPosition="1">
           <convert type="barraprogreso">FleshInfo</convert>
          </widget>
          <widget source="session.CurrentService" render="Label" position="230,190" size="475,40" zPosition="1" font="Regular; 16" halign="left" valign="center" transparent="1" noWrap="0">
            <convert type="barraprogreso">FleshInfo,Full</convert>
           </widget>
           <widget source="session.CurrentService" render="Label" position="334,235" size="70,15" zPosition="1" font="Regular; 14" halign="left" valign="center" transparent="1" noWrap="0">
            <convert type="barraprogreso">HddTemp</convert>
           </widget>
           <ePixmap alphatest="blend" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/dev_hdd.png" position="155,227" size="60,60" />
           <widget source="session.Event_Now" render="Progress" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/device.png" position="230,235" size="100,15" transparent="1" borderWidth="1" borderColor="grey" zPosition="1">
           <convert type="barraprogreso">HddInfo</convert>
          </widget>
          <widget source="session.CurrentService" render="Label" position="230,260" size="475,40" zPosition="1" font="Regular; 16" halign="left" valign="center" transparent="1" noWrap="0">
           <convert type="barraprogreso">HddInfo,Full</convert>
          </widget>
          <ePixmap alphatest="blend" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/dev_usb.png" position="155,297" size="60,60" />
          <widget source="session.Event_Now" render="Progress" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/device.png" position="230,305" size="100,15" transparent="1" borderWidth="1" borderColor="grey" zPosition="1">
           <convert type="barraprogreso">UsbInfo</convert>
          </widget>
          <widget source="session.CurrentService" render="Label" position="230,330" size="475,40" zPosition="1" font="Regular; 16" halign="left" valign="center" transparent="1" noWrap="0">
            <convert type="barraprogreso">UsbInfo,Full</convert>
          </widget>
          <ePixmap alphatest="blend" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/dev_ram.png" position="155,367" size="60,60" />
          <widget source="session.Event_Now" render="Progress" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/device.png" position="230,375" size="100,15" transparent="1" borderWidth="1" borderColor="grey" zPosition="1">
           <convert type="barraprogreso">MemTotal</convert>
          </widget>
          <widget source="session.CurrentService" render="Label" position="230,400" size="475,40" zPosition="1" font="Regular; 16" halign="left" valign="center" transparent="1" noWrap="0">
           <convert type="barraprogreso">MemTotal,Full</convert>
          </widget>
          <widget source="session.Event_Now" render="Progress" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/device.png" position="230,445" size="100,15" transparent="1" borderWidth="1" borderColor="grey" zPosition="1">
           <convert type="barraprogreso">SwapTotal</convert>
          </widget>
          <widget source="session.CurrentService" render="Label" position="230,470" size="475,40" zPosition="1" font="Regular; 16" halign="left" valign="center" transparent="1" noWrap="0">
           <convert type="barraprogreso">SwapTotal,Full</convert>
          </widget>
          <ePixmap alphatest="blend" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/dev_swap.png" position="155,437" size="60,60" />
	  <widget name="telnet_on" position="226,585" size="40,80" pixmap="/usr/share/enigma2/SF_HD/sfmenu/syteminfo/dev_ram.png" zPosition="2" alphatest="on" />
        </screen>"""

    def __init__(self, session, args = 0):
        self.skin = SFinfo.skin
        self.session = session
	Screen.__init__(self, session)
	self["actions"] = ActionMap(["SetupActions", "ColorActions", "DirectionActions"], 
			{
				"cancel": self.close,
				"ok": self.close,
			})	
	self["key_red"] = Button(_("Cancel"))	
	self['ssh_on'] = Pixmap()
	self['ssh_on'].hide()
	self['telnet_on'] = Pixmap()
	self['telnet_on'].hide()
	self['ftp_on'] = Pixmap()
	self['ftp_on'].hide()
	self['smb_on'] = Pixmap()
	self['smb_on'].hide()
	self['nfs_on'] = Pixmap()
	self['nfs_on'].hide()
	self.onLayoutFinish.append(self.updateList)

    def updateList(self):
        self.getServicesInfo()
  

    def getServicesInfo(self):
        assh = False
        atelnet = False
        aftp = False
        avpn = False
        asamba = False
        anfs = False
        rc = system('ps > /tmp/nvpn.tmp')
        if fileExists('/etc/inetd.conf'):
            f = open('/etc/inetd.conf', 'r')
            for line in f.readlines():
                parts = line.strip().split()
                if parts[0] == 'telnet':
                    atelnet = True
                if parts[0] == 'ftp':
                    aftp = True

            f.close()
        if fileExists('/tmp/nvpn.tmp'):
            f = open('/tmp/nvpn.tmp', 'r')
            for line in f.readlines():
                if line.find('/usr/sbin/openvpn') != -1:
                    avpn = True
                if line.find('/usr/sbin/dropbear') != -1:
                    assh = True
                if line.find('smbd') != -1:
                    asamba = True
                if line.find('/usr/sbin/rpc.mountd') != -1:
                    anfs = True

            f.close()
            remove('/tmp/nvpn.tmp')
        if assh == True:
            self['ssh_on'].show()
        else:
            self['ssh_on'].hide()
        if atelnet == True:
            self['telnet_on'].show()
        else:
            self['telnet_on'].hide()
        if aftp == True:
            self['ftp_on'].show()
        else:
            self['ftp_on'].hide()
        if asamba == True:
            self['smb_on'].show()
        else:
            self['smb_on'].hide()
        if anfs == True:
            self['nfs_on'].show()
        else:
            self['nfs_on'].hide()



def startinfo(session, **kwargs):
        session.open(SFinfo)  

