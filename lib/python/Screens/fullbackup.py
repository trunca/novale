#################################################################################
# FULL BACKUP UYILITY FOR ENIGMA2, SUPPORTS THE MODELS OE-A 2.0     			#
#	                         						                            #
#					MAKES A FULLBACK-UP READY FOR FLASHING.						#
#																				#
#################################################################################
from enigma import getEnigmaVersionString
from Screens.Screen import Screen
from Components.Button import Button
from Components.Label import Label
from Components.ActionMap import ActionMap
from Components.About import about
from Screens.Console import SFConsole
from Screens.MessageBox import MessageBox
from time import time, strftime, localtime
from os import path, system, makedirs, listdir, walk, statvfs
import commands
import datetime
from Tools.Directories import fileExists
import os
from SFtoolbox import getBoxType, getMachineBrand, getMachineName, getDriverDate, getImageVersion, getImageBuild, getBrandOEM, getMachineBuild, getImageFolder, getMachineUBINIZE, getMachineMKUBIFS, getMachineMtdKernel, getMachineKernelFile, getMachineRootFile, getImageFileSystem

VERSION = "Version 4.2.1 SFteam"

HaveGZkernel = True
if getBrandOEM() in ("fulan"):
	HaveGZkernel = False

def Freespace(dev):
	statdev = statvfs(dev)
	space = (statdev.f_bavail * statdev.f_frsize) / 1024
	print "[FULL BACKUP] Free space on %s = %i kilobytes" %(dev, space)
	return space

class ImageBackup(Screen):
	skin = """
	<screen position="center,center" size="560,400" title="Image Backup">
		<ePixmap position="0,360"   zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
		<ePixmap position="140,360" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
		<ePixmap position="280,360" zPosition="1" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" />
		<ePixmap position="420,360" zPosition="1" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" />
		<widget name="key_red" position="0,360" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_green" position="140,360" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_yellow" position="280,360" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="key_blue" position="420,360" zPosition="2" size="140,40" valign="center" halign="center" font="Regular;21" transparent="1" shadowColor="black" shadowOffset="-1,-1" />
		<widget name="info-hdd" position="10,30" zPosition="1" size="450,100" font="Regular;20" halign="left" valign="top" transparent="1" />
		<widget name="info-usb" position="10,150" zPosition="1" size="450,200" font="Regular;20" halign="left" valign="top" transparent="1" />
	</screen>"""
		
	def __init__(self, session, args = 0):
		Screen.__init__(self, session)
		self.session = session
		self.MODEL = getBoxType()
		self.OEM = getBrandOEM()
		self.MACHINEBUILD = getMachineBuild()
		self.MACHINENAME = getMachineName()
		self.MACHINEBRAND = getMachineBrand()
		self.IMAGEFOLDER = getImageFolder()
		self.UBINIZE_ARGS = getMachineUBINIZE()
		self.MKUBIFS_ARGS = getMachineMKUBIFS()
		self.MTDKERNEL = getMachineMtdKernel()
		self.ROOTFSBIN = getMachineRootFile()
		self.KERNELBIN = getMachineKernelFile()
		self.ROOTFSTYPE = getImageFileSystem()
		print "[FULL BACKUP] BOX MACHINEBUILD = >%s<" %self.MACHINEBUILD
		print "[FULL BACKUP] BOX MACHINENAME = >%s<" %self.MACHINENAME
		print "[FULL BACKUP] BOX MACHINEBRAND = >%s<" %self.MACHINEBRAND
		print "[FULL BACKUP] BOX MODEL = >%s<" %self.MODEL
		print "[FULL BACKUP] OEM MODEL = >%s<" %self.OEM
		print "[FULL BACKUP] IMAGEFOLDER = >%s<" %self.IMAGEFOLDER
		print "[FULL BACKUP] UBINIZE = >%s<" %self.UBINIZE_ARGS
		print "[FULL BACKUP] MKUBIFS = >%s<" %self.MKUBIFS_ARGS
		print "[FULL BACKUP] MTDKERNEL = >%s<" %self.MTDKERNEL
		print "[FULL BACKUP] ROOTFSTYPE = >%s<" %self.ROOTFSTYPE
		
		self["key_green"] = Button("USB")
		self["key_red"] = Button("HDD")
		self["key_blue"] = Button(_("Exit"))
		self["key_yellow"] = Button("Create path usb")
		self["info-usb"] = Label(_("USB = Do you want to make a back-up on USB?\nThis will take between 4 and 15 minutes depending on the used filesystem and is fully automatic.\nMake sure you first insert an USB flash drive before you select USB."))
		self["info-hdd"] = Label(_("HDD = Do you want to make an USB-back-up image on HDD? \nThis only takes 2 or 10 minutes and is fully automatic."))
		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"], 
		{
			"blue": self.quit,
			"yellow": self.yellow,
			"green": self.green,
			"red": self.red,
			"cancel": self.quit,
		}, -2)

	def check_hdd(self):
		if not path.exists("/media/hdd"):
			self.session.open(MessageBox, _("No /hdd found !!\nPlease make sure you have a HDD mounted.\n"), type = MessageBox.TYPE_ERROR)
			return False
		if Freespace('/media/hdd') < 300000:
			self.session.open(MessageBox, _("Not enough free space on /hdd !!\nYou need at least 300Mb free space.\n"), type = MessageBox.TYPE_ERROR)
			return False
		return True

	def check_usb(self, dev):
		if Freespace(dev) < 300000:
			self.session.open(MessageBox, _("Not enough free space on %s !!\nYou need at least 300Mb free space.\n" % dev), type = MessageBox.TYPE_ERROR)
			return False
		return True
		
	def quit(self):
		self.close()	
		
	def red(self):
		if self.check_hdd():
			self.doFullBackup("/hdd")

	def green(self):
		USB_DEVICE = self.SearchUSBcanidate()
		if USB_DEVICE == 'XX':
			text = _("No USB-Device found for fullbackup !!\n\n\n")
			text += _("To back-up directly to the USB-stick, the USB-stick MUST\n")
			text += _("contain a file with the name: \n\n")
			text += _("sfbackupusb or sfbackupusb.txt")
			self.session.open(MessageBox, text, type = MessageBox.TYPE_ERROR)
		else:
			if self.check_usb(USB_DEVICE):
				self.doFullBackup(USB_DEVICE)

	def yellow(self):
		if fileExists('/media/usb/sfbackupusb'):
	    		self.mbox = self.session.open(MessageBox,_("sfbackupusb existe en /media/usb"), MessageBox.TYPE_INFO, timeout = 10 )
		else:
			os.system("touch /media/usb/sfbackupusb")
			self.mbox = self.session.open(MessageBox,(_("create archivo sfbackupusb en /media/usb")), MessageBox.TYPE_INFO, timeout = 4 )

	def SearchUSBcanidate(self):
		for paths, subdirs, files in walk("/media"):
			for dir in subdirs:
				if not dir == 'hdd' and not dir == 'net':
					for file in listdir("/media/" + dir):
						if file.find("sfbackupusb") > -1:
							print "USB-DEVICE found on: /media/%s" % dir
							return "/media/" + dir						
			break
		return "XX"

	def doFullBackup(self, DIRECTORY):
		self.DIRECTORY = DIRECTORY
		self.TITLE = _("Full back-up on %s") % (self.DIRECTORY)
		self.START = time()
		self.DATE = strftime("%Y%m%d_%H%M", localtime(self.START))
		self.IMAGEVERSION = strftime("%Y%m%d", localtime(self.START))
		if "ubi" in self.ROOTFSTYPE.split():
			self.MKFS = "/usr/sbin/mkfs.ubifs"
		else:
			self.MKFS = "/usr/sbin/mkfs.jffs2"
		self.UBINIZE = "/usr/sbin/ubinize"
		self.NANDDUMP = "/usr/sbin/nanddump"
		self.WORKDIR= "%s/bi" %self.DIRECTORY
		self.TARGET="XX"

		## TESTING IF ALL THE TOOLS FOR THE BUILDING PROCESS ARE PRESENT
		if not path.exists(self.MKFS):
			text = "%s not found !!" %self.MKFS
			self.session.open(MessageBox, _(text), type = MessageBox.TYPE_ERROR)
			return
		if not path.exists(self.NANDDUMP):
			text = "%s not found !!" %self.NANDDUMP
			self.session.open(MessageBox, _(text), type = MessageBox.TYPE_ERROR)
			return

		self.SHOWNAME = "%s %s" %(self.MACHINEBRAND, self.MODEL)
		self.MAINDESTOLD = "%s/%s" %(self.DIRECTORY, self.MODEL)
		self.MAINDEST = "%s/%s" %(self.DIRECTORY,self.IMAGEFOLDER)
		self.EXTRA = "%s/fullbackup_%s/%s/%s" % (self.DIRECTORY, self.MODEL, self.DATE, self.IMAGEFOLDER)
		self.EXTRAOLD = "%s/fullbackup_%s/%s/%s" % (self.DIRECTORY, self.MODEL, self.DATE, self.MODEL)


		self.message = "echo -e '\n"
		self.message += (_("Back-up Tool for a %s\n" %self.SHOWNAME)).upper()
		self.message += VERSION + '\n'
		self.message += "_________________________________________________\n\n"
		self.message += _("Please be patient, a backup will now be made,\n")
		if self.ROOTFSTYPE == "ubi":
			self.message += _("because of the used filesystem the back-up\n")
			self.message += _("will take about 3-12 minutes for this system\n")
		else:
			self.message += _("this will take between 2 and 9 minutes\n")
		self.message += "\n_________________________________________________\n\n"
		self.message += "'"

		## PREPARING THE BUILDING ENVIRONMENT
		system("rm -rf %s" %self.WORKDIR)
		if not path.exists(self.WORKDIR):
			makedirs(self.WORKDIR)
		if not path.exists("/tmp/bi/root"):
			makedirs("/tmp/bi/root")
		system("sync")
		system("mount --bind / /tmp/bi/root")

		if "jffs2" in self.ROOTFSTYPE.split():
			cmd1 = "%s --root=/tmp/bi/root --faketime --output=%s/root.jffs2 %s" % (self.MKFS, self.WORKDIR, self.MKUBIFS_ARGS)
			cmd2 = None
		else:
			f = open("%s/ubinize.cfg" %self.WORKDIR, "w")
			f.write("[ubifs]\n")
			f.write("mode=ubi\n")
			f.write("image=%s/root.ubi\n" %self.WORKDIR)
			f.write("vol_id=0\n")
			f.write("vol_type=dynamic\n")
			f.write("vol_name=rootfs\n")
			f.write("vol_flags=autoresize\n")
			f.close()
			ff = open("%s/root.ubi" %self.WORKDIR, "w")
			ff.close()
			cmd1 = "%s -r /tmp/bi/root -o %s/root.ubi %s" % (self.MKFS, self.WORKDIR, self.MKUBIFS_ARGS)
			cmd2 = "%s -o %s/root.ubifs %s %s/ubinize.cfg" % (self.UBINIZE, self.WORKDIR, self.UBINIZE_ARGS, self.WORKDIR)
			cmd3 = "mv %s/root.ubifs %s/root.%s" %(self.WORKDIR, self.WORKDIR, self.ROOTFSTYPE)

		cmdlist = []
		cmdlist.append(self.message)
		cmdlist.append('echo "Create: root.%s\n"' %self.ROOTFSTYPE)
		cmdlist.append(cmd1)
		if cmd2:
			cmdlist.append(cmd2)
			cmdlist.append(cmd3)
		cmdlist.append("chmod 644 %s/root.%s" %(self.WORKDIR, self.ROOTFSTYPE))
		cmdlist.append('echo " "')
		cmdlist.append('echo "Create: kerneldump"')
		cmdlist.append('echo " "')
		cmdlist.append("nanddump -a -f %s/vmlinux.gz /dev/%s" % (self.WORKDIR, self.MTDKERNEL))
		cmdlist.append('echo " "')
		
		if HaveGZkernel:
			cmdlist.append('echo "Check: kerneldump"')
		cmdlist.append("sync")

		self.session.open(SFConsole, title = self.TITLE, cmdlist = cmdlist, finishedCallback = self.doFullBackupCB, closeOnSuccess = True)

	def doFullBackupCB(self):
		if HaveGZkernel:
			ret = commands.getoutput(' gzip -d %s/vmlinux.gz -c > /tmp/vmlinux.bin' % self.WORKDIR)
			if ret:
				text = "Kernel dump error\n"
				text += "Please Flash your Kernel new and Backup again"
				system('rm -rf /tmp/vmlinux.bin')
				self.session.open(MessageBox, _(text), type = MessageBox.TYPE_ERROR)
				return

		cmdlist = []
		cmdlist.append(self.message)
		if HaveGZkernel:
			cmdlist.append('echo "Kernel dump OK"')
			cmdlist.append("rm -rf /tmp/vmlinux.bin")
		cmdlist.append('echo "_________________________________________________"')
		cmdlist.append('echo "Almost there... "')
		cmdlist.append('echo "Now building the USB-Image"')

		system('rm -rf %s' %self.MAINDEST)
		if not path.exists(self.MAINDEST):
			makedirs(self.MAINDEST)
		if not path.exists(self.EXTRA):
			makedirs(self.EXTRA)

		f = open("%s/imageversion" %self.MAINDEST, "w")
		f.write(self.IMAGEVERSION)
		f.close()

		system('mv %s/root.%s %s/%s' %(self.WORKDIR, self.ROOTFSTYPE, self.MAINDEST, self.ROOTFSBIN))
		system('mv %s/vmlinux.gz %s/%s' %(self.WORKDIR, self.MAINDEST, self.KERNELBIN))
		cmdlist.append('echo "rename this file to "force" to force an update without confirmation" > %s/noforce' %self.MAINDEST)

		if self.MODEL in ("gbquad", "gbquadplus", "gb800ue", "gb800ueplus", "gbultraue", "twinboxlcd"):
			lcdwaitkey = '/usr/share/lcdwaitkey.bin'
			lcdwarning = '/usr/share/lcdwarning.bin'
			if path.exists(lcdwaitkey):
				system('cp %s %s/lcdwaitkey.bin' %(lcdwaitkey, self.MAINDEST))
			if path.exists(lcdwarning):
				system('cp %s %s/lcdwarning.bin' %(lcdwarning, self.MAINDEST))
		if self.MODEL == "gb800solo":
			burnbat = "%s/fullbackup_%s/%s" % (self.DIRECTORY, self.MODEL, self.DATE)
			f = open("%s/burn.bat" % (burnbat), "w")
			f.write("flash -noheader usbdisk0:gigablue/solo/kernel.bin flash0.kernel\n")
			f.write("flash -noheader usbdisk0:gigablue/solo/rootfs.bin flash0.rootfs\n")
			f.write('setenv -p STARTUP "boot -z -elf flash0.kernel: ')
			f.write("'rootfstype=jffs2 bmem=106M@150M root=/dev/mtdblock6 rw '")
			f.write('"\n')
			f.close()

		cmdlist.append('cp -r %s/* %s/' % (self.MAINDEST, self.EXTRA))

		cmdlist.append("sync")
		file_found = True

		if not path.exists("%s/%s" % (self.MAINDEST, self.ROOTFSBIN)):
			print 'ROOTFS bin file not found'
			file_found = False

		if not path.exists("%s/%s" % (self.MAINDEST, self.KERNELBIN)):
			print 'KERNEL bin file not found'
			file_found = False

		if path.exists("%s/noforce" % self.MAINDEST):
			print 'NOFORCE bin file not found'
			file_found = False

		if file_found:
			cmdlist.append('echo "_________________________________________________\n"')
			cmdlist.append('echo "USB Image created on:" %s' %self.MAINDEST)
			cmdlist.append('echo "and there is made an extra copy on:"')
			cmdlist.append('echo %s' %self.EXTRA)
			cmdlist.append('echo "_________________________________________________\n"')
			cmdlist.append('echo " "')
			cmdlist.append('echo "\nPlease wait...almost ready! "')
			cmdlist.append('echo " "')
			cmdlist.append('echo "To restore the image:"')
			cmdlist.append('echo "Please check the manual of the receiver"')
			cmdlist.append('echo "on how to restore the image"')
		else:
			cmdlist.append('echo "_________________________________________________\n"')
			cmdlist.append('echo "Image creation failed - "')
			cmdlist.append('echo "Probable causes could be"')
			cmdlist.append('echo "     wrong back-up destination "')
			cmdlist.append('echo "     no space left on back-up device"')
			cmdlist.append('echo "     no writing permission on back-up device"')
			cmdlist.append('echo " "')

		if self.DIRECTORY == "/hdd":
			self.TARGET = self.SearchUSBcanidate()
			print "TARGET = %s" % self.TARGET
			if self.TARGET == 'XX':
				cmdlist.append('echo " "')
			else:
				cmdlist.append('echo "_________________________________________________\n"')
				cmdlist.append('echo " "')
				cmdlist.append('echo "There is a valid USB-flash drive detected in one "')
				cmdlist.append('echo "of the USB-ports, therefor an extra copy of the "')
				cmdlist.append('echo "back-up image will now be copied to that USB- "')
				cmdlist.append('echo "flash drive. "')
				cmdlist.append('echo "This only takes about 1 or 2 minutes"')
				cmdlist.append('echo " "')

				cmdlist.append('mkdir -p %s/%s' % (self.TARGET, self.IMAGEFOLDER))
				cmdlist.append('cp -r %s %s/' % (self.MAINDEST, self.TARGET))


				cmdlist.append("sync")
				cmdlist.append('echo "Backup finished and copied to your USB-flash drive"')
			
		cmdlist.append("umount /tmp/bi/root")
		cmdlist.append("rmdir /tmp/bi/root")
		cmdlist.append("rmdir /tmp/bi")
		cmdlist.append("rm -rf %s" % self.WORKDIR)
		cmdlist.append("sleep 5")
		END = time()
		DIFF = int(END - self.START)
		TIMELAP = str(datetime.timedelta(seconds=DIFF))
		cmdlist.append('echo " Time required for this process: %s"' %TIMELAP)

		self.session.open(SFConsole, title = self.TITLE, cmdlist = cmdlist, closeOnSuccess = False)

def getChipSetString():
	if getBoxType() in ('dm7080','dm820'):
		return "7435"
	else:
		try:
			f = open('/proc/stb/info/chipset', 'r')
			chipset = f.read()
			f.close()
			return str(chipset.lower().replace('\n','').replace('bcm','').replace('brcm','').replace('sti',''))
		except IOError:
			return "unavailable"

def getCPUString():
	if getBoxType() in ('xc7362'):
		return "Broadcom"
	else:
		try:
			system="unknown"
			file = open('/proc/cpuinfo', 'r')
			lines = file.readlines()
			for x in lines:
				splitted = x.split(': ')
				if len(splitted) > 1:
					splitted[1] = splitted[1].replace('\n','')
					if splitted[0].startswith("system type"):
						system = splitted[1].split(' ')[0]
					elif splitted[0].startswith("Processor"):
						system = splitted[1].split(' ')[0]
			file.close()
			return system
		except IOError:
			return "unavailable"

def getCpuCoresString():
	try:
		file = open('/proc/cpuinfo', 'r')
		lines = file.readlines()
		for x in lines:
			splitted = x.split(': ')
			if len(splitted) > 1:
				splitted[1] = splitted[1].replace('\n','')
				if splitted[0].startswith("processor"):
					if int(splitted[1]) > 0:
						cores = 2
					else:
						cores = 1
		file.close()
		return cores
	except IOError:
		return "unavailable"

def getKernelVersionString():
	try:
		f = open("/proc/version","r")
		kernelversion = f.read().split(' ', 4)[2].split('-',2)[0]
		f.close()
		return kernelversion
	except:
		return _("unknown")


	def imageInfo(self):
		AboutText = _("Full Image Backup ")
		AboutText += _("sfteam") + "\n"
		AboutText += _("Support at") + " http://foros.sfteam.es/\n\n"
		AboutText += _("[Image Info]\n")
		AboutText += _("Model: %s %s\n") % (getMachineBrand(), getMachineName())
		AboutText += _("Backup Date: %s\n") % strftime("%Y-%m-%d", localtime(self.START))

		if path.exists('/proc/stb/info/chipset'):
			AboutText += _("Chipset: BCM%s") % about.getChipSetString().lower().replace('\n','').replace('bcm','') + "\n"

		AboutText += _("CPU: %s") % about.getCPUString() + "\n"
		AboutText += _("Cores: %s") % about.getCpuCoresString() + "\n"

		AboutText += _("Version: %s") % getImageVersion() + "\n"
		AboutText += _("Build: %s") % getImageBuild() + "\n"
		AboutText += _("Kernel: %s") % about.getKernelVersionString() + "\n"

		string = getDriverDate()
		year = string[0:4]
		month = string[4:6]
		day = string[6:8]
		driversdate = '-'.join((year, month, day))
		AboutText += _("Drivers:\t%s") % driversdate + "\n"

		AboutText += _("Last update:\t%s") % getEnigmaVersionString() + "\n\n"

		AboutText += _("[Enigma2 Settings]\n")
		AboutText += commands.getoutput("cat /etc/enigma2/settings")
		AboutText += _("\n\n[User - bouquets (TV)]\n")
		try:
			f = open("/etc/enigma2/bouquets.tv","r")
			lines = f.readlines()
			f.close()
			for line in lines:
				if line.startswith("#SERVICE:"):
					bouqet = line.split()
					if len(bouqet) > 3:
						bouqet[3] = bouqet[3].replace('"','')
						f = open("/etc/enigma2/" + bouqet[3],"r")
						userbouqet = f.readline()
						AboutText += userbouqet.replace('#NAME ','')
						f.close()
		except:
			AboutText += "Error reading bouquets.tv"
			
		AboutText += _("\n[User - bouquets (RADIO)]\n")
		try:
			f = open("/etc/enigma2/bouquets.radio","r")
			lines = f.readlines()
			f.close()
			for line in lines:
				if line.startswith("#SERVICE:"):
					bouqet = line.split()
					if len(bouqet) > 3:
						bouqet[3] = bouqet[3].replace('"','')
						f = open("/etc/enigma2/" + bouqet[3],"r")
						userbouqet = f.readline()
						AboutText += userbouqet.replace('#NAME ','')
						f.close()
		except:
			AboutText += "Error reading bouquets.radio"

		AboutText += _("\n[Installed Plugins]\n")
		AboutText += commands.getoutput("opkg list_installed | grep enigma2-plugin-")

		return AboutText

