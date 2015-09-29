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

class BackupPanel(Screen):
    skin = ' \n\t<screen name="sfteambckScreen" position="center,center" size="560,450" title="Backup to USB" >  \n\t<widget name="information" position="10,10" size="540,180" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;18"  />\n\t<ePixmap name="red" position="85,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />\n\t<ePixmap name="green" position="330,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />\n\t<widget name="key_red" position="20,405" size="270,50" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;21"  />\n\t<widget name="key_green" position="265,405" size="270,50" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;21"  />\n\t</screen> \n\t'

    def __init__(self, session, picPath = None):
        Screen.__init__(self, session)
        print '[sfteambckScreen] __init__\n'
        self.picPath = picPath
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self['sftPic'] = Pixmap()
        self['information'] = Label('')
        self['information'].text = _('\n\n\n\nInstructions\n------------------------------\n\n1) Insert the USB stick in your receiver\n2) En caso necesario monte como usb pulsando boton azul\n3) Click OK to start the process')
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.cancel,
	 'blue': self.mount,
         'green': self.preHaceBackup,
         'red': self.cancel}, -1)
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('OK'))
	self['key_blue'] = Label(_('Mount'))
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.onLayoutFinish.append(self.ShowPicture)

    def preHaceBackup(self):
        self.session.openWithCallback(self.HaceBackup, MessageBox, _('This process will make a backup of the installed image to a USB flash drive.\n\nDo you want to continue?'), MessageBox.TYPE_YESNO, timeout=15, default=False)

    def mount(self):
        import Mount
        self.session.open(Mount.HddMount)

    def HaceBackup(self, ret):
        cmdusb = '/usr/bin/backup /media/usb'
        if ret:
            self.session.open(SFConsole, _('Backup to USB'), [cmdusb])
            self.close()

    def ShowPicture(self):
        if self.picPath is not None:
            self.PicLoad.setPara([self['sftPic'].instance.size().width(),
             self['sftPic'].instance.size().height(),
             self.Scale[0],
             self.Scale[1],
             0,
             1,
             '#002C2C39'])
            self.PicLoad.startDecode(self.picPath)
        return

    def DecodePicture(self, PicInfo = ''):
        if self.picPath is not None:
            ptr = self.PicLoad.getData()
            self['sftPic'].instance.setPixmap(ptr)
        return

    def cancel(self):
        print '[sfteamScreen] - cancel\n'
        self.close(None)
        return

class BackupPanelhdd(Screen):
    skin = ' \n\t<screen name="sfteambckScreen" position="center,center" size="560,450" title="Backup to HDD" >  \n\t<widget name="information" position="10,10" size="540,180" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;18"  />\n\t<ePixmap name="red" position="85,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />\n\t<ePixmap name="green" position="330,410" zPosition="1" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />\n\t<widget name="key_red" position="20,405" size="270,50" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;21"  />\n\t<widget name="key_green" position="265,405" size="270,50" halign="center" valign="center" transparent="1" zPosition="2"  font="Regular;21"  />\n\t</screen> \n\t'

    def __init__(self, session, picPath = None):
        Screen.__init__(self, session)
        print '[sfteambckScreen] __init__\n'
        self.picPath = picPath
        self.Scale = AVSwitch().getFramebufferScale()
        self.PicLoad = ePicLoad()
        self['sftPic'] = Pixmap()
        self['information'] = Label('')
        self['information'].text = _('\n\n\n\nInstructions\n------------------------------\n\n1) Mount HDD in your receiver\n2) En caso necesario monte como HDD pulsando boton azul\n3) Click OK to start the process')
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'cancel': self.cancel,
	 'blue': self.mount,
         'green': self.preHaceBackup,
         'red': self.cancel}, -1)
        self['key_red'] = Label(_('Cancel'))
        self['key_green'] = Label(_('OK'))
	self['key_blue'] = Label(_('Mount'))
        self.PicLoad.PictureData.get().append(self.DecodePicture)
        self.onLayoutFinish.append(self.ShowPicture)

    def preHaceBackup(self):
        self.session.openWithCallback(self.HaceBackup, MessageBox, _('This process will make a backup of the installed image to a HDD flash drive.\n\nDo you want to continue?'), MessageBox.TYPE_YESNO, timeout=15, default=False)

    def mount(self):
        import Mount
        self.session.open(Mount.HddMount)

    def HaceBackup(self, ret):
        cmdhdd = '/usr/bin/backup /media/HDD'
        if ret:
            self.session.open(SFConsole, _('Backup to HDD'), [cmdhdd])
            self.close()

    def ShowPicture(self):
        if self.picPath is not None:
            self.PicLoad.setPara([self['sftPic'].instance.size().width(),
             self['sftPic'].instance.size().height(),
             self.Scale[0],
             self.Scale[1],
             0,
             1,
             '#002C2C39'])
            self.PicLoad.startDecode(self.picPath)
        return

    def DecodePicture(self, PicInfo = ''):
        if self.picPath is not None:
            ptr = self.PicLoad.getData()
            self['sftPic'].instance.setPixmap(ptr)
        return

    def cancel(self):
        print '[sfteamScreen] - cancel\n'
        self.close(None)
        return
