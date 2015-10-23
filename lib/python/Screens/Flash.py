from Plugins.SystemPlugins.Hotplug.plugin import hotplugNotifier
from Components.Button import Button
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.FileList import FileList
from Components.Task import Task, Job, job_manager, Condition
from Components.Sources.StaticText import StaticText
from Screens.Console import SFConsole2
from Screens.MessageBoxSF import MessageBoxSF
from Screens.ChoiceBox import ChoiceBox
from Screens.Screen import Screen
from Screens.Console import SFConsole2
from Screens.HelpMenu import HelpableScreen
from Screens.TaskView import JobView
from Tools.Downloader import downloadWithProgress
import urllib2
import os
import shutil
import math
from SFtoolbox import getBoxType,  getImageDistro, getMachineName, getMachineBrand, getImageVersion
distro =  getImageDistro()
ImageVersion = getImageVersion()

ImageVersion3 = ''
if getMachineBrand() == "Vu+":
	ImageVersion3= os.popen("cat /etc/opkg/mips32el-feed.conf | grep -o -e 4.2gl -e 4.2-old").read().rstrip()

#############################################################################################################
image = 0 # 0=SFTeamBeta / 1=SFTeamStable
if distro.lower() == "sfteam":
	image = 1
elif distro.lower() == "sfteambeta":
	image = 0

feedurl_sft = 'https://releases.soldiersat.eu/4.2.1'
feedurl_sft2 = 'https://releases.soldiersat.eu/4.2.1'
imagePath = '/media/usb/images'
flashPath = '/media/usb/images/flash'
flashTmp = '/media/usb/images/tmp'
ofgwritePath = '/usr/bin/ofgwrite'
#############################################################################################################

def Freespace(dev):
	statdev = os.statvfs(dev)
	space = (statdev.f_bavail * statdev.f_frsize) / 1024
	print "[Flash Online] Free space on %s = %i kilobytes" %(dev, space)
	return space

def ReadNewfeed():
	f = open('/etc/enigma2/newfeed', 'r')
	newfeed = f.readlines()
	f.close()
	return newfeed

class FlashOnline(Screen):
	skin = """
	<screen position="center,center" size="560,450" title="Flash On the Fly">
		<ePixmap position="35,410"   zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap position="210,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap position="385,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
		<widget name="key_red" position="35,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_green" position="210,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_yellow" position="385,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="info-online" position="10,30" zPosition="1" size="450,100" font="Regular;20" halign="left" valign="top" transparent="1" />
		<widget name="info-local" position="10,150" zPosition="1" size="450,200" font="Regular;20" halign="left" valign="top" transparent="1" />
	</screen>"""
		
	def __init__(self, session):
		Screen.__init__(self, session)
		self.session = session

		Screen.setTitle(self, _("Flash On the Fly"))
		self["key_yellow"] = Button("Local")
		self["key_green"] = Button("Online")
		self["key_red"] = Button(_("Exit"))
		self["key_blue"] = Button("")
		self["info-local"] = Label(_("Local = Flash a image from local path /hdd/images"))
		self["info-online"] = Label(_("Online = Download a image and flash it"))

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], 
		{
			"blue": self.blue,
			"yellow": self.yellow,
			"green": self.green,
			"red": self.quit,
			"cancel": self.quit,
		}, -2)

	def check_hdd(self):
		if not os.path.exists("/media/usb"):
			self.session.open(MessageBoxSF, _("No /hdd found !!\nPlease make sure you have a HDD mounted.\n\nExit plugin."), type = MessageBoxSF.TYPE_ERROR)
			return False
		if Freespace('/media/usb') < 300000:
			self.session.open(MessageBoxSF, _("Not enough free space on /hdd !!\nYou need at least 300Mb free space.\n\nExit plugin."), type = MessageBoxSF.TYPE_ERROR)
			return False
		if not os.path.exists(ofgwritePath):
			self.session.open(MessageBoxSF, _('ofgwrite not found !!\nPlease make sure you have ofgwrite installed in /usr/bin/ofgwrite.\n\nExit plugin.'), type = MessageBoxSF.TYPE_ERROR)
			return False

		if not os.path.exists(imagePath):
			try:
				os.mkdir(imagePath)
			except:
				pass
		
		if os.path.exists(flashPath):
			try:
				os.system('rm -rf ' + flashPath)
			except:
				pass
		try:
			os.mkdir(flashPath)
		except:
			pass
		return True

	def quit(self):
		self.close()
		
	def blue(self):
		pass

	def green(self):
		if self.check_hdd():
			self.session.open(doFlashImage, online = True)
		else:
			self.close()

	def yellow(self):
		if self.check_hdd():
			self.session.open(doFlashImageLocal, online = False)
		else:
			self.close()

class doFlashImage(Screen):
	skin = """
	<screen position="center,center" size="560,450" title="Flash On the fly (select a image)">
		<ePixmap position="35,410"   zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap position="210,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap position="385,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
		<widget name="key_red" position="35,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_green" position="210,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_yellow" position="385,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
        <widget name="imagen-online" position="10,20" zPosition="1" size="540,25" font="Regular;20" halign="center" valign="top" foregroundColor="#ffff00" transparent="0" />
		<widget name="imageList" position="10,60" zPosition="1" size="540,400" font="Regular;20" scrollbarMode="showOnDemand" transparent="1" />
	</screen>"""
		
	def __init__(self, session, online ):
		Screen.__init__(self, session)
		self.session = session

		Screen.setTitle(self, _("Flash On the fly (select a image)"))
		self["key_green"] = Button(_("Flash"))
		self["key_red"] = Button(_("Exit"))
		self["key_yellow"] = Button("")
		self["imagen-online"] = Label(_("Download image and flash it"))
            
		self.filename = None
		self.imagelist = []
		self.simulate = False
		self.Online = online
		self.imagePath = imagePath
		self.feedurl = feedurl_sft
		if image == 0:
			self.feed = "sft2"
		else:
			self.feed = "sft"
		self["imageList"] = MenuList(self.imagelist)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], 
		{
			"green": self.green,
			"yellow": self.yellow,
			"red": self.quit,
			"blue": self.blue,
			"cancel": self.quit,
		}, -2)
		self.onLayoutFinish.append(self.layoutFinished)
		self.newfeed = None
		if os.path.exists('/etc/enigma2/newfeed'):
			self.newfeed = ReadNewfeed()

		
	def quit(self):
		self.close()
		
	def blue(self):
		if self.Online:
			if image == 1:
				if self.feed == "sftbeta":
					self.feed = "sft"
				else:
					self.feed = "sftbeta"
			else:
				if self.feed == "sftbeta":
					self.feed = "sftbeta2"
				else:
					self.feed = "sftbeta"
			self.layoutFinished()
			return
		sel = self["imageList"].l.getCurrentSelection()
		if sel == None:
			print"Nothing to select !!"
			return
		self.filename = sel
		self.session.openWithCallback(self.RemoveCB, MessageBoxSF, _("Do you really want to delete\n%s ?") % (sel), MessageBoxSF.TYPE_YESNO)

	def RemoveCB(self, ret):
		if ret:
			if os.path.exists(self.imagePath + "/" + self.filename):
				os.remove(self.imagePath + "/" + self.filename)
			self.imagelist.remove(self.filename)
			self["imageList"].l.setList(self.imagelist)
		
	def box(self):
		box = getBoxType()
		machinename = getMachineName()
		if box in ('uniboxhd1', 'uniboxhd2', 'uniboxhd3'):
			box = "ventonhdx"
		elif box == 'odinm6':
			box = getMachineName().lower()
		elif box == "inihde" and machinename.lower() == "xpeedlx":
			box = "xpeedlx"
		elif box in ('xpeedlx1', 'xpeedlx2'):
			box = "xpeedlx"
		elif box == "inihde" and machinename.lower() == "hd-1000":
			box = "sezam-1000hd"
		elif box == "ventonhdx" and machinename.lower() == "hd-5000":
			box = "sezam-5000hd"
		elif box == "ventonhdx" and machinename.lower() == "premium twin":
			box = "miraclebox-twin"
		elif box == "xp1000" and machinename.lower() == "sf8 hd":
			box = "sf8"
		elif box.startswith('et') and not box in ('et8000', 'et8500', 'et8500s', 'et10000'):
			box = box[0:3] + 'x00'
		elif box == 'odinm9' and self.feed == "sftbeta":
			box = 'maram9'
		return box

	def green(self, ret = None):
		sel = self["imageList"].l.getCurrentSelection()
		if sel == None:
			print"Nothing to select !!"
			return
		file_name = self.imagePath + "/" + sel
		self.filename = file_name
		self.sel = sel
		box = self.box()
		self.hide()
		if self.Online:
			url = self.feedurl + "/" + box + "/" + sel
			print "[Flash Online] Download image: >%s<" % url
			if self.newfeed:
				self.feedurl = self.newfeed[0][:-1]
				url = self.feedurl + "/" + box + "/" + sel
				authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
				authinfo.add_password(None, self.feedurl, self.newfeed[1][:-1], self.newfeed[2][:-1])
				handler = urllib2.HTTPBasicAuthHandler(authinfo)
				myopener = urllib2.build_opener(handler)
				opened = urllib2.install_opener(myopener)
				u = urllib2.urlopen(url)
				total_size = int(u.info().getheaders("Content-Length")[0])
				downloaded = 0
				CHUNK = 256 * 1024
				with open(file_name, 'wb') as fp:
					while True:
						chunk = u.read(CHUNK)
						downloaded += len(chunk)
						print "Downloading: %s Bytes of %s" % (downloaded, total_size)
						if not chunk: break
						fp.write(chunk)
				self.ImageDownloadCB(False)
			else:
				try:
					u = urllib2.urlopen(url)
					f = open(file_name, 'wb')
					f.close()
					job = ImageDownloadJob(url, file_name, sel)
					job.afterEvent = "close"
					job_manager.AddJob(job)
					job_manager.failed_jobs = []
					self.session.openWithCallback(self.ImageDownloadCB, JobView, job, backgroundable = False, afterEventChangeable = False)
				except urllib2.URLError as e:
					print "[Flash Online] Download failed !!\n%s" % e
					self.session.openWithCallback(self.ImageDownloadCB, MessageBoxSF, _("Download Failed !!" + "\n%s" % e), type = MessageBoxSF.TYPE_ERROR)
					self.close()
		else:
			self.session.openWithCallback(self.startInstallLocal, MessageBoxSF, _("Do you want to backup your settings now?"), default=False)
			

	def ImageDownloadCB(self, ret):
		if ret:
			return
		if job_manager.active_job:
			job_manager.active_job = None
			self.close()
			return
		if len(job_manager.failed_jobs) == 0:
			self.flashWithPostFlashActionMode = 'online'
			self.flashWithPostFlashAction()
		else:
			self.session.open(MessageBoxSF, _("Download Failed !!"), type = MessageBoxSF.TYPE_ERROR)

	def flashWithPostFlashAction(self, ret = True):
		if ret:
			print "flashWithPostFlashAction"
			title =_("Please select what to do after flashing the image:\n(In addition, if it exists, a local script will be executed as well at /media/usb/images/config/myrestore.sh)")
			list = ((_("Flash and start installation wizard"), "wizard"),
			(_("Flash and restore settings and no plugins"), "restoresettingsnoplugin"),
			(_("Flash and restore settings and selected plugins (ask user)"), "restoresettings"),
			(_("Flash and restore settings and all saved plugins"), "restoresettingsandallplugins"),
			(_("Do not flash image"), "abort"))
			self.session.openWithCallback(self.postFlashActionCallback, ChoiceBox,title=title,list=list,selection=self.SelectPrevPostFashAction())
		else:
			self.show()

	def SelectPrevPostFashAction(self):
		index = 0
		Settings = False
		AllPlugins = False
		noPlugins = False
		
		if os.path.exists('/media/usb/images/config/settings'):
			Settings = True
		if os.path.exists('/media/usb/images/config/plugins'):
			AllPlugins = True
		if os.path.exists('/media/usb/images/config/noplugins'):
			noPlugins = True

		if 	Settings and noPlugins:
			index = 1
		elif Settings and not AllPlugins and not noPlugins:
			index = 2
		elif Settings and AllPlugins:
			index = 3

		return index

	def postFlashActionCallback(self, answer):
		print "postFlashActionCallback"
		restoreSettings   = False
		restoreAllPlugins = False
		restoreSettingsnoPlugin = False
		if answer is not None:
			if answer[1] == "restoresettings":
				restoreSettings   = True
			if answer[1] == "restoresettingsnoplugin":
				restoreSettings = True
				restoreSettingsnoPlugin = True
			if answer[1] == "restoresettingsandallplugins":
				restoreSettings   = True
				restoreAllPlugins = True
			if restoreSettings:
				self.SaveEPG()
			if answer[1] != "abort":
				if restoreSettings:
					try:
						os.system('mkdir -p /media/usb/images/config')
						os.system('touch /media/usb/images/config/settings')
					except:
						print "postFlashActionCallback: failed to create /media/usb/images/config/settings"
				else:
					if os.path.exists('/media/usb/images/config/settings'):
						os.system('rm -f /media/usb/images/config/settings')
				if restoreAllPlugins:
					try:
						os.system('mkdir -p /media/usb/images/config')
						os.system('touch /media/usb/images/config/plugins')
					except:
						print "postFlashActionCallback: failed to create /media/usb/images/config/plugins"
				else:
					if os.path.exists('/media/usb/images/config/plugins'):
						os.system('rm -f /media/usb/images/config/plugins')
				if restoreSettingsnoPlugin:
					try:
						os.system('mkdir -p /media/usb/images/config')
						os.system('touch /media/usb/images/config/noplugins')
					except:
						print "postFlashActionCallback: failed to create /media/usb/images/config/noplugins"
				else:
					if os.path.exists('/media/usb/images/config/noplugins'):
						os.system('rm -f /media/usb/images/config/noplugins')
				if self.flashWithPostFlashActionMode == 'online':
					self.unzip_image(self.filename, flashPath)
				else:
					self.startInstallLocalCB()
			else:
				self.show()
		else:
			self.show()

	def unzip_image(self, filename, path):
		print "Unzip %s to %s" %(filename,path)
		self.session.openWithCallback(self.cmdFinished, SFConsole2, title = _("Unzipping files, Please wait ..."), cmdlist = ['unzip ' + filename + ' -o -d ' + path, "sleep 3"], closeOnSuccess = True)

	def cmdFinished(self):
		self.prepair_flashtmp(flashPath)
		self.Start_Flashing()

	def Start_Flashing(self):
		print "Start Flashing"
		if os.path.exists(ofgwritePath):
			text = _("Flashing: ")
			if self.simulate:
				text += _("Simulate (no write)")
				cmd = "%s -n -r -k %s > /dev/null 2>&1" % (ofgwritePath, flashTmp)
				self.close()
				message = "echo -e '\n"
				message += _('Show only found image and mtd partitions.\n')
				message += "'"
			else:
				text += _("root and kernel")
				cmd = "%s -r -k %s > /dev/null 2>&1" % (ofgwritePath, flashTmp)
				message = "echo -e '\n"
				message += _('ofgwrite will stop enigma2 now to run the flash.\n')
				message += _('Your STB will freeze during the flashing process.\n')
				message += _('Please: DO NOT reboot your STB and turn off the power.\n')
				message += _('The image or kernel will be flashing and auto booted in few minutes.\n')
				if self.box() == 'gb800solo':
					message += _('GB800SOLO takes about 20 mins !!\n')
				message += "'"
			self.session.open(SFConsole2, text,[message, cmd])

	def prepair_flashtmp(self, tmpPath):
		if os.path.exists(flashTmp):
			flashTmpold = flashTmp + 'old'
			os.system('mv %s %s' %(flashTmp, flashTmpold))
			os.system('rm -rf %s' %flashTmpold)
		if not os.path.exists(flashTmp):
			os.mkdir(flashTmp)
		kernel = True
		rootfs = True
		
		for path, subdirs, files in os.walk(tmpPath):
			for name in files:
				if name.find('kernel') > -1 and name.endswith('.bin') and kernel:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/kernel.bin'
					shutil.copyfile(binfile, dest)
					kernel = False
				elif name.find('root') > -1 and (name.endswith('.bin') or name.endswith('.jffs2')) and rootfs:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/rootfs.bin'
					shutil.copyfile(binfile, dest)
					rootfs = False
				elif name.find('uImage') > -1 and kernel:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/uImage'
					shutil.copyfile(binfile, dest)
					kernel = False
				elif name.find('e2jffs2') > -1 and name.endswith('.img') and rootfs:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/e2jffs2.img'
					shutil.copyfile(binfile, dest)
					rootfs = False
					
	def yellow(self):
		if not self.Online:
			self.session.openWithCallback(self.DeviceBrowserClosed, DeviceBrowser, None, matchingPattern="^.*\.(zip|bin|jffs2|img)", showDirectories=True, showMountpoints=True, inhibitMounts=["/autofs/sr0/"])
		else:
			from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen
			self.session.openWithCallback(self.green,BackupScreen, runBackup = True)

	def startInstallLocal(self, ret = None):
		if ret:
			from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen
			self.flashWithPostFlashActionMode = 'local'
			self.session.openWithCallback(self.flashWithPostFlashAction,BackupScreen, runBackup = True)
		else:
			self.flashWithPostFlashActionMode = 'local'
			self.flashWithPostFlashAction()

	def startInstallLocalCB(self, ret = None):
		if self.sel == str(flashTmp):
			self.Start_Flashing()
		else:
			self.unzip_image(self.filename, flashPath)

	def DeviceBrowserClosed(self, path, filename, binorzip):
		if path:
			print path, filename, binorzip
			strPath = str(path)
			if strPath[-1] == '/':
				strPath = strPath[:-1]
			self.imagePath = strPath
			if os.path.exists(flashTmp):
				os.system('rm -rf ' + flashTmp)
			os.mkdir(flashTmp)
			if binorzip == 0:
				for files in os.listdir(self.imagePath):
					if files.endswith(".bin") or files.endswith('.jffs2') or files.endswith('.img'):
						self.prepair_flashtmp(strPath)
						break
				self.Start_Flashing()
			elif binorzip == 1:
				self.unzip_image(strPath + '/' + filename, flashPath)
			else:
				self.layoutFinished()
	
		else:
			self.imagePath = imagePath

	def layoutFinished(self):
		box = self.box()
		self.imagelist = []

		if self.Online:
			self["key_yellow"].setText("Backup&Flash")
			
			url = '%s/%s' % (self.feedurl,box)
			try:
				req = urllib2.Request(url)
				if self.newfeed:
					self.feedurl = self.newfeed[0][:-1]
					url = '%s/%s' % (self.feedurl,box)
					authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
					authinfo.add_password(None, self.feedurl, self.newfeed[1][:-1], self.newfeed[2][:-1])
					handler = urllib2.HTTPBasicAuthHandler(authinfo)
					myopener = urllib2.build_opener(handler)
					opened = urllib2.install_opener(myopener)
					response = urllib2.urlopen(url)
				else:
					response = urllib2.urlopen(req)
			except urllib2.URLError as e:
				print "URL ERROR: %s\n%s" % (e,url)
				self["imageList"].l.setList(self.imagelist)
				return

			try:
				the_page = response.read()

			except urllib2.HTTPError as e:
				print "HTTP download ERROR: %s" % e.code
				return

			lines = the_page.split('\n')
			tt = len(box)
			for line in lines:
				if line.find("<tr><td valign=\"top\"><a href=\"") > -1:
					t1 = line.find("<tr><td valign=\"top\"><a href=\"")
					t2 = line.find(".zip")
					self.imagelist.append(line[t1+30:t2+4])
		else:
			self["key_blue"].setText(_("Delete"))
			self["key_yellow"].setText(_("Devices"))
			for name in os.listdir(self.imagePath):
				if name.endswith(".zip"): # and name.find(box) > 1:
					self.imagelist.append(name)
			self.imagelist.sort()
			if os.path.exists(flashTmp):
				for file in os.listdir(flashTmp):
					if file.find(".bin") > -1:
						self.imagelist.insert( 0, str(flashTmp))
						break

		self["imageList"].l.setList(self.imagelist)

	def SaveEPG(self):
		from enigma import eEPGCache
		epgcache = eEPGCache.getInstance()
		epgcache.save()

class doFlashImageLocal(Screen):
	skin = """
	<screen position="center,center" size="560,450" title="Flash On the fly (select a image)">
		<ePixmap position="0,410"   zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap position="140,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap position="280,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
		<ePixmap position="420,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
		<widget name="key_red" position="0,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_green" position="140,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_yellow" position="280,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_blue" position="420,410" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
        <widget name="imagen-online" position="10,20" zPosition="1" size="540,25" font="Regular;20" halign="center" valign="top" foregroundColor="#ffff00" transparent="0" />
		<widget name="imageList" position="10,60" zPosition="1" size="540,400" font="Regular;20" scrollbarMode="showOnDemand" transparent="1" />
	</screen>"""
		
	def __init__(self, session, online ):
		Screen.__init__(self, session)
		self.session = session

		Screen.setTitle(self, _("Flash On the fly (select a image)"))
		self["key_green"] = Button(_("Flash"))
		self["key_red"] = Button(_("Exit"))
		self["key_blue"] = Button("")
		self["key_yellow"] = Button("")
		self["imagen-online"] = Label(_("Select image and flash it"))
            
		self.filename = None
		self.imagelist = []
		self.simulate = False
		self.Online = online
		self.imagePath = imagePath
		self.feedurl = feedurl_sft
		if image == 0:
			self.feed = "sft2"
		else:
			self.feed = "sft"
		self["imageList"] = MenuList(self.imagelist)
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], 
		{
			"green": self.green,
			"yellow": self.yellow,
			"red": self.quit,
			"blue": self.blue,
			"cancel": self.quit,
		}, -2)
		self.onLayoutFinish.append(self.layoutFinished)
		self.newfeed = None
		if os.path.exists('/etc/enigma2/newfeed'):
			self.newfeed = ReadNewfeed()

		
	def quit(self):
		self.close()
		
	def blue(self):
		if self.Online:
			if image == 1:
				if self.feed == "sftbeta":
					self.feed = "sft"
				else:
					self.feed = "sftbeta"
			else:
				if self.feed == "sftbeta":
					self.feed = "sftbeta2"
				else:
					self.feed = "sftbeta"
			self.layoutFinished()
			return
		sel = self["imageList"].l.getCurrentSelection()
		if sel == None:
			print"Nothing to select !!"
			return
		self.filename = sel
		self.session.openWithCallback(self.RemoveCB, MessageBoxSF, _("Do you really want to delete\n%s ?") % (sel), MessageBoxSF.TYPE_YESNO)

	def RemoveCB(self, ret):
		if ret:
			if os.path.exists(self.imagePath + "/" + self.filename):
				os.remove(self.imagePath + "/" + self.filename)
			self.imagelist.remove(self.filename)
			self["imageList"].l.setList(self.imagelist)
		
	def box(self):
		box = getBoxType()
		machinename = getMachineName()
		if box in ('uniboxhd1', 'uniboxhd2', 'uniboxhd3'):
			box = "ventonhdx"
		elif box == 'odinm6':
			box = getMachineName().lower()
		elif box == "inihde" and machinename.lower() == "xpeedlx":
			box = "xpeedlx"
		elif box in ('xpeedlx1', 'xpeedlx2'):
			box = "xpeedlx"
		elif box == "inihde" and machinename.lower() == "hd-1000":
			box = "sezam-1000hd"
		elif box == "ventonhdx" and machinename.lower() == "hd-5000":
			box = "sezam-5000hd"
		elif box == "ventonhdx" and machinename.lower() == "premium twin":
			box = "miraclebox-twin"
		elif box == "xp1000" and machinename.lower() == "sf8 hd":
			box = "sf8"
		elif box.startswith('et') and not box in ('et8000', 'et8500', 'et8500s', 'et10000'):
			box = box[0:3] + 'x00'
		elif box == 'odinm9' and self.feed == "sftbeta":
			box = 'maram9'
		return box

	def green(self, ret = None):
		sel = self["imageList"].l.getCurrentSelection()
		if sel == None:
			print"Nothing to select !!"
			return
		file_name = self.imagePath + "/" + sel
		self.filename = file_name
		self.sel = sel
		box = self.box()
		self.hide()
		if self.Online:
			url = self.feedurl + "/" + box + "/" + sel
			print "[Flash Online] Download image: >%s<" % url
			if self.newfeed:
				self.feedurl = self.newfeed[0][:-1]
				url = self.feedurl + "/" + box + "/" + sel
				authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
				authinfo.add_password(None, self.feedurl, self.newfeed[1][:-1], self.newfeed[2][:-1])
				handler = urllib2.HTTPBasicAuthHandler(authinfo)
				myopener = urllib2.build_opener(handler)
				opened = urllib2.install_opener(myopener)
				u = urllib2.urlopen(url)
				total_size = int(u.info().getheaders("Content-Length")[0])
				downloaded = 0
				CHUNK = 256 * 1024
				with open(file_name, 'wb') as fp:
					while True:
						chunk = u.read(CHUNK)
						downloaded += len(chunk)
						print "Downloading: %s Bytes of %s" % (downloaded, total_size)
						if not chunk: break
						fp.write(chunk)
				self.ImageDownloadCB(False)
			else:
				try:
					u = urllib2.urlopen(url)
					f = open(file_name, 'wb')
					f.close()
					job = ImageDownloadJob(url, file_name, sel)
					job.afterEvent = "close"
					job_manager.AddJob(job)
					job_manager.failed_jobs = []
					self.session.openWithCallback(self.ImageDownloadCB, JobView, job, backgroundable = False, afterEventChangeable = False)
				except urllib2.URLError as e:
					print "[Flash Online] Download failed !!\n%s" % e
					self.session.openWithCallback(self.ImageDownloadCB, MessageBoxSF, _("Download Failed !!" + "\n%s" % e), type = MessageBoxSF.TYPE_ERROR)
					self.close()
		else:
			self.session.openWithCallback(self.startInstallLocal, MessageBoxSF, _("Do you want to backup your settings now?"), default=False)
			

	def ImageDownloadCB(self, ret):
		if ret:
			return
		if job_manager.active_job:
			job_manager.active_job = None
			self.close()
			return
		if len(job_manager.failed_jobs) == 0:
			self.flashWithPostFlashActionMode = 'online'
			self.flashWithPostFlashAction()
		else:
			self.session.open(MessageBoxSF, _("Download Failed !!"), type = MessageBoxSF.TYPE_ERROR)

	def flashWithPostFlashAction(self, ret = True):
		if ret:
			print "flashWithPostFlashAction"
			title =_("Please select what to do after flashing the image:\n(In addition, if it exists, a local script will be executed as well at /media/usb/images/config/myrestore.sh)")
			list = ((_("Flash and start installation wizard"), "wizard"),
			(_("Flash and restore settings and no plugins"), "restoresettingsnoplugin"),
			(_("Flash and restore settings and selected plugins (ask user)"), "restoresettings"),
			(_("Flash and restore settings and all saved plugins"), "restoresettingsandallplugins"),
			(_("Do not flash image"), "abort"))
			self.session.openWithCallback(self.postFlashActionCallback, ChoiceBox,title=title,list=list,selection=self.SelectPrevPostFashAction())
		else:
			self.show()

	def SelectPrevPostFashAction(self):
		index = 0
		Settings = False
		AllPlugins = False
		noPlugins = False
		
		if os.path.exists('/media/usb/images/config/settings'):
			Settings = True
		if os.path.exists('/media/usb/images/config/plugins'):
			AllPlugins = True
		if os.path.exists('/media/usb/images/config/noplugins'):
			noPlugins = True

		if 	Settings and noPlugins:
			index = 1
		elif Settings and not AllPlugins and not noPlugins:
			index = 2
		elif Settings and AllPlugins:
			index = 3

		return index

	def postFlashActionCallback(self, answer):
		print "postFlashActionCallback"
		restoreSettings   = False
		restoreAllPlugins = False
		restoreSettingsnoPlugin = False
		if answer is not None:
			if answer[1] == "restoresettings":
				restoreSettings   = True
			if answer[1] == "restoresettingsnoplugin":
				restoreSettings = True
				restoreSettingsnoPlugin = True
			if answer[1] == "restoresettingsandallplugins":
				restoreSettings   = True
				restoreAllPlugins = True
			if restoreSettings:
				self.SaveEPG()
			if answer[1] != "abort":
				if restoreSettings:
					try:
						os.system('mkdir -p /media/usb/images/config')
						os.system('touch /media/usb/images/config/settings')
					except:
						print "postFlashActionCallback: failed to create /media/usb/images/config/settings"
				else:
					if os.path.exists('/media/usb/images/config/settings'):
						os.system('rm -f /media/usb/images/config/settings')
				if restoreAllPlugins:
					try:
						os.system('mkdir -p /media/usb/images/config')
						os.system('touch /media/usb/images/config/plugins')
					except:
						print "postFlashActionCallback: failed to create /media/usb/images/config/plugins"
				else:
					if os.path.exists('/media/usb/images/config/plugins'):
						os.system('rm -f /media/usb/images/config/plugins')
				if restoreSettingsnoPlugin:
					try:
						os.system('mkdir -p /media/usb/images/config')
						os.system('touch /media/usb/images/config/noplugins')
					except:
						print "postFlashActionCallback: failed to create /media/usb/images/config/noplugins"
				else:
					if os.path.exists('/media/usb/images/config/noplugins'):
						os.system('rm -f /media/usb/images/config/noplugins')
				if self.flashWithPostFlashActionMode == 'online':
					self.unzip_image(self.filename, flashPath)
				else:
					self.startInstallLocalCB()
			else:
				self.show()
		else:
			self.show()

	def unzip_image(self, filename, path):
		print "Unzip %s to %s" %(filename,path)
		self.session.openWithCallback(self.cmdFinished, SFConsole2, title = _("Unzipping files, Please wait ..."), cmdlist = ['unzip ' + filename + ' -o -d ' + path, "sleep 3"], closeOnSuccess = True)

	def cmdFinished(self):
		self.prepair_flashtmp(flashPath)
		self.Start_Flashing()

	def Start_Flashing(self):
		print "Start Flashing"
		if os.path.exists(ofgwritePath):
			text = _("Flashing: ")
			if self.simulate:
				text += _("Simulate (no write)")
				cmd = "%s -n -r -k %s > /dev/null 2>&1" % (ofgwritePath, flashTmp)
				self.close()
				message = "echo -e '\n"
				message += _('Show only found image and mtd partitions.\n')
				message += "'"
			else:
				text += _("root and kernel")
				cmd = "%s -r -k %s > /dev/null 2>&1" % (ofgwritePath, flashTmp)
				message = "echo -e '\n"
				message += _('ofgwrite will stop enigma2 now to run the flash.\n')
				message += _('Your STB will freeze during the flashing process.\n')
				message += _('Please: DO NOT reboot your STB and turn off the power.\n')
				message += _('The image or kernel will be flashing and auto booted in few minutes.\n')
				if self.box() == 'gb800solo':
					message += _('GB800SOLO takes about 20 mins !!\n')
				message += "'"
			self.session.open(SFConsole2, text,[message, cmd])

	def prepair_flashtmp(self, tmpPath):
		if os.path.exists(flashTmp):
			flashTmpold = flashTmp + 'old'
			os.system('mv %s %s' %(flashTmp, flashTmpold))
			os.system('rm -rf %s' %flashTmpold)
		if not os.path.exists(flashTmp):
			os.mkdir(flashTmp)
		kernel = True
		rootfs = True
		
		for path, subdirs, files in os.walk(tmpPath):
			for name in files:
				if name.find('kernel') > -1 and name.endswith('.bin') and kernel:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/kernel.bin'
					shutil.copyfile(binfile, dest)
					kernel = False
				elif name.find('root') > -1 and (name.endswith('.bin') or name.endswith('.jffs2')) and rootfs:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/rootfs.bin'
					shutil.copyfile(binfile, dest)
					rootfs = False
				elif name.find('uImage') > -1 and kernel:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/uImage'
					shutil.copyfile(binfile, dest)
					kernel = False
				elif name.find('e2jffs2') > -1 and name.endswith('.img') and rootfs:
					binfile = os.path.join(path, name)
					dest = flashTmp + '/e2jffs2.img'
					shutil.copyfile(binfile, dest)
					rootfs = False
					
	def yellow(self):
		if not self.Online:
			self.session.openWithCallback(self.DeviceBrowserClosed, DeviceBrowser, None, matchingPattern="^.*\.(zip|bin|jffs2|img)", showDirectories=True, showMountpoints=True, inhibitMounts=["/autofs/sr0/"])
		else:
			from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen
			self.session.openWithCallback(self.green,BackupScreen, runBackup = True)

	def startInstallLocal(self, ret = None):
		if ret:
			from Plugins.SystemPlugins.SoftwareManager.BackupRestore import BackupScreen
			self.flashWithPostFlashActionMode = 'local'
			self.session.openWithCallback(self.flashWithPostFlashAction,BackupScreen, runBackup = True)
		else:
			self.flashWithPostFlashActionMode = 'local'
			self.flashWithPostFlashAction()

	def startInstallLocalCB(self, ret = None):
		if self.sel == str(flashTmp):
			self.Start_Flashing()
		else:
			self.unzip_image(self.filename, flashPath)

	def DeviceBrowserClosed(self, path, filename, binorzip):
		if path:
			print path, filename, binorzip
			strPath = str(path)
			if strPath[-1] == '/':
				strPath = strPath[:-1]
			self.imagePath = strPath
			if os.path.exists(flashTmp):
				os.system('rm -rf ' + flashTmp)
			os.mkdir(flashTmp)
			if binorzip == 0:
				for files in os.listdir(self.imagePath):
					if files.endswith(".bin") or files.endswith('.jffs2') or files.endswith('.img'):
						self.prepair_flashtmp(strPath)
						break
				self.Start_Flashing()
			elif binorzip == 1:
				self.unzip_image(strPath + '/' + filename, flashPath)
			else:
				self.layoutFinished()
	
		else:
			self.imagePath = imagePath

	def layoutFinished(self):
		box = self.box()
		self.imagelist = []
		if self.Online:
			
			self["key_yellow"].setText("Backup&Flash")
			
			url = '%s/%s' % (self.feedurl,box)
			try:
				req = urllib2.Request(url)
				if self.newfeed:
					self.feedurl = self.newfeed[0][:-1]
					url = '%s/%s' % (self.feedurl,box)
					authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()
					authinfo.add_password(None, self.feedurl, self.newfeed[1][:-1], self.newfeed[2][:-1])
					handler = urllib2.HTTPBasicAuthHandler(authinfo)
					myopener = urllib2.build_opener(handler)
					opened = urllib2.install_opener(myopener)
					response = urllib2.urlopen(url)
				else:
					response = urllib2.urlopen(req)
			except urllib2.URLError as e:
				print "URL ERROR: %s\n%s" % (e,url)
				self["imageList"].l.setList(self.imagelist)
				return

			try:
				the_page = response.read()

			except urllib2.HTTPError as e:
				print "HTTP download ERROR: %s" % e.code
				return

			lines = the_page.split('\n')
			tt = len(box)
			for line in lines:
				if line.find("<tr><td valign=\"top\"><a href=\"") > -1:
					t1 = line.find("<tr><td valign=\"top\"><a href=\"")
					t2 = line.find(".zip")
					self.imagelist.append(line[t+30:t2+4])
		else:
			self["key_blue"].setText(_("Delete"))
			self["key_yellow"].setText(_("Devices"))
			for name in os.listdir(self.imagePath):
				if name.endswith(".zip"): # and name.find(box) > 1:
					self.imagelist.append(name)
			self.imagelist.sort()
			if os.path.exists(flashTmp):
				for file in os.listdir(flashTmp):
					if file.find(".bin") > -1:
						self.imagelist.insert( 0, str(flashTmp))
						break

		self["imageList"].l.setList(self.imagelist)

	def SaveEPG(self):
		from enigma import eEPGCache
		epgcache = eEPGCache.getInstance()
		epgcache.save()


class ImageDownloadJob(Job):
	def __init__(self, url, filename, file):
		Job.__init__(self, _("Downloading %s" %file))
		ImageDownloadTask(self, url, filename)

class DownloaderPostcondition(Condition):
	def check(self, task):
		return task.returncode == 0

	def getErrorMessage(self, task):
		return self.error_message

class ImageDownloadTask(Task):
	def __init__(self, job, url, path):
		Task.__init__(self, job, _("Downloading"))
		self.postconditions.append(DownloaderPostcondition())
		self.job = job
		self.url = url
		self.path = path
		self.error_message = ""
		self.last_recvbytes = 0
		self.error_message = None
		self.download = None
		self.aborted = False

	def run(self, callback):
		self.callback = callback
		self.download = downloadWithProgress(self.url,self.path)
		self.download.addProgress(self.download_progress)
		self.download.start().addCallback(self.download_finished).addErrback(self.download_failed)
		print "[ImageDownloadTask] downloading", self.url, "to", self.path

	def abort(self):
		print "[ImageDownloadTask] aborting", self.url
		if self.download:
			self.download.stop()
		self.aborted = True

	def download_progress(self, recvbytes, totalbytes):
		if ( recvbytes - self.last_recvbytes  ) > 10000: # anti-flicker
			self.progress = int(100*(float(recvbytes)/float(totalbytes)))
			self.name = _("Downloading") + ' ' + "%d of %d kBytes" % (recvbytes/1024, totalbytes/1024)
			self.last_recvbytes = recvbytes

	def download_failed(self, failure_instance=None, error_message=""):
		self.error_message = error_message
		if error_message == "" and failure_instance is not None:
			self.error_message = failure_instance.getErrorMessage()
		Task.processFinished(self, 1)

	def download_finished(self, string=""):
		if self.aborted:
			self.finish(aborted = True)
		else:
			Task.processFinished(self, 0)

class DeviceBrowser(Screen, HelpableScreen):
	skin = """
		<screen name="DeviceBrowser" position="center,center" size="560,450" >
			<ePixmap pixmap="skin_default/buttons/red.png" position="85,410" size="140,40" alphatest="on" />
			<ePixmap pixmap="skin_default/buttons/green.png" position="330,410" size="140,40" alphatest="on" />
			<widget source="key_red" render="Label" position="20,410" zPosition="1" size="270,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />
			<widget source="key_green" render="Label" position="265,410" zPosition="1" size="270,40" font="Regular;20" halign="center" valign="center" backgroundColor="#1f771f" transparent="1" />
        	<widget name="imagen-online" position="10,20" zPosition="1" size="540,25" font="Regular;20" halign="center" valign="top" foregroundColor="#ffff00" transparent="0" />
			<widget name="filelist" position="10,60" size="540,340" scrollbarMode="showOnDemand" />
		</screen>"""

	def __init__(self, session, startdir, message="", showDirectories = True, showFiles = True, showMountpoints = True, matchingPattern = "", useServiceRef = False, inhibitDirs = False, inhibitMounts = False, isTop = False, enableWrapAround = False, additionalExtensions = None):
		Screen.__init__(self, session)

		HelpableScreen.__init__(self)
		Screen.setTitle(self, _("Please select medium"))

		self["key_red"] = StaticText(_("Cancel"))
		self["key_green"] = StaticText()
		self["imagen-online"] = Label(_("Search image and flash it"))

		self.filelist = FileList(startdir, showDirectories = showDirectories, showFiles = showFiles, showMountpoints = showMountpoints, matchingPattern = matchingPattern, useServiceRef = useServiceRef, inhibitDirs = inhibitDirs, inhibitMounts = inhibitMounts, isTop = isTop, enableWrapAround = enableWrapAround, additionalExtensions = additionalExtensions)
		self["filelist"] = self.filelist

		self["FilelistActions"] = ActionMap(["SetupActions", "ColorActions"],
			{
				"green": self.use,
				"red": self.exit,
				"ok": self.ok,
				"cancel": self.exit
			})

		hotplugNotifier.append(self.hotplugCB)
		self.onShown.append(self.updateButton)
		self.onClose.append(self.removeHotplug)

	def hotplugCB(self, dev, action):
		print "[hotplugCB]", dev, action
		self.updateButton()

	def updateButton(self):

		if self["filelist"].getFilename() or self["filelist"].getCurrentDirectory():
			self["key_green"].text = _("Flash")
		else:
			self["key_green"].text = ""

	def removeHotplug(self):
		print "[removeHotplug]"
		hotplugNotifier.remove(self.hotplugCB)

	def ok(self):
		if self.filelist.canDescent():
			if self["filelist"].showMountpoints == True and self["filelist"].showDirectories == False:
				self.use()
			else:
				self.filelist.descent()

	def use(self):
		print "[use]", self["filelist"].getCurrentDirectory(), self["filelist"].getFilename()
		if self["filelist"].getFilename() is not None and self["filelist"].getCurrentDirectory() is not None:
			if self["filelist"].getFilename().endswith(".bin") or self["filelist"].getFilename().endswith(".jffs2"):
				self.close(self["filelist"].getCurrentDirectory(), self["filelist"].getFilename(), 0)
			elif self["filelist"].getFilename().endswith(".zip"):
				self.close(self["filelist"].getCurrentDirectory(), self["filelist"].getFilename(), 1)
			else:
				return

	def exit(self):
		self.close(False, False, -1)
