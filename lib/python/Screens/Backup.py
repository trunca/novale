from enigma import *
from Screens.Screen import Screen
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.MessageBox import MessageBox
from Components.Pixmap import Pixmap
from Components.AVSwitch import AVSwitch
from Components.Pixmap import Pixmap
from Components.Button import Button
from enigma import ePicLoad
from enigma import eServiceCenter, eServiceReference
from ServiceReference import ServiceReference
from Components.ServiceList import ServiceList
from Plugins.Plugin import PluginDescriptor
from Screens.Console import SFConsole
from Screens.MessageBox import MessageBox

from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE


###########################################################################

cmd = "/usr/bin/backup /media/usb"


class BackupPanel(Screen):
	skin = """ 
	<screen name="sfteambckScreen" position="center,center" size="560,450" title="Backup to USB" >  
	<widget name="information" position="10,10" size="540,180" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;18"  />
	<ePixmap name="red" position="85,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
	<ePixmap name="green" position="330,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
	<widget name="key_red" position="20,405" size="270,50" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;21"  />
	<widget name="key_green" position="265,405" size="270,50" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;21"  />
	</screen> 
	"""		

	def __init__(self, session, picPath = None):	

		
		Screen.__init__(self, session)
		print "[sfteambckScreen] __init__\n"
		self.picPath = picPath
		self.Scale = AVSwitch().getFramebufferScale()
		self.PicLoad = ePicLoad()
		self["sftPic"] = Pixmap()
		self["information"] = Label("")
		self["information"].text = _("\n\n\n\nInstructions\n------------------------------\n\n1) Insert the USB stick in your receiver\n2) Click OK to start the process") 		

		self["actions"] = ActionMap(["OkCancelActions", "ColorActions"],
			{
				"cancel": self.cancel,
				"green": self.preHaceBackup,
				"red": self.cancel,
			},-1)
		
		self["key_red"] = Label(_("Cancel"))
		self["key_green"] = Label(_("OK"))

		self.PicLoad.PictureData.get().append(self.DecodePicture)
		self.onLayoutFinish.append(self.ShowPicture)

	def preHaceBackup(self):
		self.session.openWithCallback(self.HaceBackup, MessageBox, _('This process will make a backup of the installed image to a USB flash drive.\n\nDo you want to continue?'), MessageBox.TYPE_YESNO, timeout=15, default=False)
		
	def HaceBackup(self, ret):
		if ret:
				self.session.open(SFConsole,_("Backup to USB"),[cmd])
				self.close()
		

	def ShowPicture(self):
		if self.picPath is not None:
			self.PicLoad.setPara([
						self["sftPic"].instance.size().width(),
						self["sftPic"].instance.size().height(),
						self.Scale[0],
						self.Scale[1],
						0,
						1,
						"#002C2C39"])
						
			self.PicLoad.startDecode(self.picPath)

	def DecodePicture(self, PicInfo = ""):
		if self.picPath is not None:
			ptr = self.PicLoad.getData()
			self["sftPic"].instance.setPixmap(ptr)


	def cancel(self):
		print "[sfteamScreen] - cancel\n"
		self.close(None)

