from Screens.Screen import Screen
from Screens.Console import Console
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Screens.Console import SFConsole
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
from Components.ActionMap import ActionMap
from Components.config import getConfigListEntry, config, ConfigSubsection, ConfigText, ConfigSelection, ConfigInteger, ConfigClock, NoSave, configfile
from Components.ConfigList import ConfigListScreen
from Components.Label import Label
from Components.Sources.List import List
from Components.Pixmap import Pixmap
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.Console import Console
from os import system, listdir, rename, symlink, unlink, path, mkdir
from time import sleep
from os import environ
import os
import sys

class MediatombPanel(Screen):
    skin = '\n\t\t<screen position="center,center" size="590,400" title="mediatomb">\n\t\t\t<widget name="lab1" position="10,0" size="100,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labdisabled" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labactive" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2" />\n\t\t\t<widget name="lab2" position="240,0" size="150,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labstop" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labrun" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2"/>\n\t\t\t<widget source="list" render="Listbox" position="10,35" size="540,325" scrollbarMode="showOnDemand" >\n\t\t\t\t<convert type="StringList" />\n\t\t\t</widget>\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="150,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="300,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="450,350" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget name="key_yellow" position="150,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_green" position="300,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_blue" position="450,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
	Screen.__init__(self, session)
        Screen.setTitle(self, _('mediatomb'))
        self['lab1'] = Label(_('Autostart:'))
        self['labactive'] = Label(_(_('Active')))
        self['labdisabled'] = Label(_(_('Disabled')))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self.Console = Console()
        self.my_mediatomb_active = False
        self.my_mediatomb_run = False
	self['key_red'] = Label(_('Close'))
        self['key_yellow'] = Label(_('Start'))
        self['key_blue'] = Label(_('Autostart'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'MenuActions'], {'back': self.close,
         'red': self.close,
         'yellow': self.mediatombStart,
         'blue': self.autostart})
        self.onLayoutFinish.append(self.updateList)

    def mediatombStart(self):
        if self.my_mediatomb_run == False:
            self.session.open(SFConsole, title=_('Start Mediatomb'), cmdlist=['/etc/init.d/mediatomb start'])
            sleep(3)
            self.updateList()
        elif self.my_mediatomb_run == True:
            self.session.open(SFConsole, title=_('Stop Mediatomb'), cmdlist=['/etc/init.d/mediatomb stop'])
            sleep(3)
            self.updateList()

    def autostart(self):
        if path.exists('/etc/rc0.d/K90mediatomb'):
            unlink('/etc/rc0.d/K90mediatomb')
        else:
            symlink('/etc/init.d/mediatomb', '/etc/rc0.d/K90mediatomb')
        if path.exists('/etc/rc1.d/K90mediatomb'):
            unlink('/etc/rc1.d/K90mediatomb')
        else:
            symlink('/etc/init.d/mediatomb', '/etc/rc1.d/K90mediatomb')
        if path.exists('/etc/rc2.d/S90mediatomb'):
            unlink('/etc/rc2.d/S90mediatomb')
        else:
            symlink('/etc/init.d/mediatomb', '/etc/rc2.d/S90mediatomb')
        if path.exists('/etc/rc3.d/S90mediatomb'):
            unlink('/etc/rc3.d/S90mediatomb')
        else:
            symlink('/etc/init.d/mediatomb', '/etc/rc3.d/S90mediatomb')
        if path.exists('/etc/rc4.d/S90mediatomb'):
            unlink('/etc/rc4.d/S90mediatomb')
        else:
            symlink('/etc/init.d/mediatomb', '/etc/rc4.d/S90mediatomb')
        if path.exists('/etc/rc5.d/S90mediatomb'):
            unlink('/etc/rc5.d/S90mediatomb')
        else:
            symlink('/etc/init.d/mediatomb', '/etc/rc5.d/S90mediatomb')
        if path.exists('/etc/rc6.d/K90mediatomb'):
            unlink('/etc/rc6.d/K90mediatomb')
        else:
            symlink('/etc/init.d/mediatomb', '/etc/rc6.d/K90mediatomb')
        self.updateList()

    
    def updateList(self):
        import process
        p = process.ProcessList()
        mediatomb_process = str(p.named('mediatomb')).strip('[]')
        self['labrun'].hide()
        self['labstop'].hide()
        self['labactive'].hide()
        self['labdisabled'].hide()
        self.my_mediatomb_active = False
        self.my_mediatomb_run = False
        if path.exists('/etc/rc3.d/S90mediatomb'):
            self['labdisabled'].hide()
            self['labactive'].show()
            self.my_mediatomb_active = True
        else:
            self['labactive'].hide()
            self['labdisabled'].show()
        if mediatomb_process:
            self.my_mediatomb_run = True
        if self.my_mediatomb_run == True:
            self['labstop'].hide()
            self['labrun'].show()
            self['key_yellow'].setText(_('Stop'))
        else:
            self['labstop'].show()
            self['labrun'].hide()
            self['key_yellow'].setText(_('Start'))
        self.list = []
        
    def quit(self):
        self.close()
            

class xupnpdpanel(Screen):
    skin = '\n\t\t<screen position="center,center" size="590,400" title="xupnpd">\n\t\t\t<widget name="lab1" position="10,0" size="100,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labdisabled" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labactive" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2" />\n\t\t\t<widget name="lab2" position="240,0" size="150,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labstop" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labrun" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2"/>\n\t\t\t<widget source="list" render="Listbox" position="10,35" size="540,325" scrollbarMode="showOnDemand" >\n\t\t\t\t<convert type="StringList" />\n\t\t\t</widget>\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="150,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="300,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="450,350" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget name="key_yellow" position="150,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_green" position="300,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_blue" position="450,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
	Screen.__init__(self, session)
        Screen.setTitle(self, _('xupnpd'))
        self['lab1'] = Label(_('Autostart:'))
        self['labactive'] = Label(_(_('Active')))
        self['labdisabled'] = Label(_(_('Disabled')))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self.Console = Console()
        self.my_xupnpd_active = False
        self.my_xupnpd_run = False
	self['key_red'] = Label(_('Close'))
        self['key_yellow'] = Label(_('Start'))
        self['key_blue'] = Label(_('Autostart'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'MenuActions'], {'back': self.close,
	 'red': self.close,
         'yellow': self.xupnpdStart,
         'blue': self.autostart})
        self.onLayoutFinish.append(self.updateList)

    def xupnpdStart(self):
        if self.my_xupnpd_run == False:
            self.session.open(SFConsole, title=_('Start xupnpd'), cmdlist=['/etc/init.d/xupnpd start'])
            sleep(3)
            self.updateList()
        elif self.my_xupnpd_run == True:
            self.session.open(SFConsole, title=_('Stop xupnpd'), cmdlist=['/etc/init.d/xupnpd stop'])
            sleep(3)
            self.updateList()

    def autostart(self):
        if path.exists('/etc/rc0.d/K20xupnpd'):
            unlink('/etc/rc0.d/K20xupnpd')
        else:
            symlink('/etc/init.d/xupnpd', '/etc/rc0.d/K20xupnpd')
        if path.exists('/etc/rc1.d/K20xupnpd'):
            unlink('/etc/rc1.d/K20xupnpd')
        else:
            symlink('/etc/init.d/xupnpd', '/etc/rc1.d/K20xupnpd')
        if path.exists('/etc/rc2.d/S20xupnpd'):
            unlink('/etc/rc2.d/S20xupnpd')
        else:
            symlink('/etc/init.d/xupnpd', '/etc/rc2.d/S20xupnpd')
        if path.exists('/etc/rc3.d/S20xupnpd'):
            unlink('/etc/rc3.d/S20xupnpd')
        else:
            symlink('/etc/init.d/xupnpd', '/etc/rc3.d/S20xupnpd')
        if path.exists('/etc/rc4.d/S20xupnpd'):
            unlink('/etc/rc4.d/S20xupnpd')
        else:
            symlink('/etc/init.d/xupnpd', '/etc/rc4.d/S20xupnpd')
        if path.exists('/etc/rc5.d/S20xupnpd'):
            unlink('/etc/rc5.d/S20xupnpd')
        else:
            symlink('/etc/init.d/xupnpd', '/etc/rc5.d/S20xupnpd')
        if path.exists('/etc/rc6.d/K20xupnpd'):
            unlink('/etc/rc6.d/K20xupnpd')
        else:
            symlink('/etc/init.d/xupnpd', '/etc/rc6.d/K20xupnpd')
        self.updateList()

    
    def updateList(self):
        import process
        p = process.ProcessList()
        xupnpd_process = str(p.named('xupnpd')).strip('[]')
        self['labrun'].hide()
        self['labstop'].hide()
        self['labactive'].hide()
        self['labdisabled'].hide()
        self.my_xupnpd_active = False
        self.my_xupnpd_run = False
        if path.exists('/etc/rc3.d/S20xupnpd'):
            self['labdisabled'].hide()
            self['labactive'].show()
            self.my_xupnpd_active = True
        else:
            self['labactive'].hide()
            self['labdisabled'].show()
        if xupnpd_process:
            self.my_xupnpd_run = True
        if self.my_xupnpd_run == True:
            self['labstop'].hide()
            self['labrun'].show()
            self['key_yellow'].setText(_('Stop'))
        else:
            self['labstop'].show()
            self['labrun'].hide()
            self['key_yellow'].setText(_('Start'))
        self.list = []
        
    def quit(self):
        self.close()

class udpxypanel(Screen):
    skin = '\n\t\t<screen position="center,center" size="590,400" title="Udpxy">\n\t\t\t<widget name="lab1" position="10,0" size="100,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labdisabled" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labactive" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2" />\n\t\t\t<widget name="lab2" position="240,0" size="150,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labstop" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labrun" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2"/>\n\t\t\t<widget source="list" render="Listbox" position="10,35" size="540,325" scrollbarMode="showOnDemand" >\n\t\t\t\t<convert type="StringList" />\n\t\t\t</widget>\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="150,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="300,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="450,350" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget name="key_yellow" position="150,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_green" position="300,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_blue" position="450,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
	Screen.__init__(self, session)
        Screen.setTitle(self, _('udpxy'))
        self['lab1'] = Label(_('Autostart:'))
        self['labactive'] = Label(_(_('Active')))
        self['labdisabled'] = Label(_(_('Disabled')))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self.Console = Console()
        self.my_udpxy_active = False
        self.my_udpxy_run = False
        self['key_green'] = Label(_('Reset Ch.'))
        self['key_red'] = Label(_('Path Ch. Ip'))
        self['key_yellow'] = Label(_('Start'))
        self['key_blue'] = Label(_('Autostart'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'MenuActions'], {'back': self.close,
         'green': self.udpxyreset,
         'red': self.udpxyip,
         'yellow': self.udpxyStart,
         'blue': self.autostart})
        self.onLayoutFinish.append(self.updateList)

    def udpxyip(self):
            os.system("/usr/bin/patip.sh")
	    self.mbox = self.session.open(MessageBox,_("Chanel list patch IP, restart GUI"), MessageBox.TYPE_INFO, timeout = 20 )

    def udpxyreset(self):
            os.system("rm -r /etc/enigma2/userbouquet.iptv.tv")
            os.system("cp /usr/lib/enigma2/python/Screens/SFextra/scripts/userbouquet.iptv.tv /etc/enigma2/userbouquet.iptv.tv")
            self.mbox = self.session.open(MessageBox,_("Chanel list reset"), MessageBox.TYPE_INFO, timeout = 20 )

    def udpxyStart(self):
        if self.my_udpxy_run == False:
            self.session.open(SFConsole, title=_('Start udpxy'), cmdlist=['/etc/init.d/udpxy start'])
            sleep(3)
            self.updateList()
        elif self.my_udpxy_run == True:
            self.session.open(SFConsole, title=_('Stop udpxy'), cmdlist=['/etc/init.d/udpxy stop'])
            sleep(3)
            self.updateList()

    def autostart(self):
        if path.exists('/etc/rc0.d/K20udpxy'):
            unlink('/etc/rc0.d/K20udpxy')
        else:
            symlink('/etc/init.d/udpxy', '/etc/rc0.d/K20udpxy')
        if path.exists('/etc/rc1.d/K20udpxy'):
            unlink('/etc/rc1.d/K20udpxy')
        else:
            symlink('/etc/init.d/udpxy', '/etc/rc1.d/K20udpxy')
        if path.exists('/etc/rc2.d/S20udpxy'):
            unlink('/etc/rc2.d/S20udpxy')
        else:
            symlink('/etc/init.d/udpxy', '/etc/rc2.d/S20udpxy')
        if path.exists('/etc/rc3.d/S20udpxy'):
            unlink('/etc/rc3.d/S20udpxy')
        else:
            symlink('/etc/init.d/udpxy', '/etc/rc3.d/S20udpxy')
        if path.exists('/etc/rc4.d/S20udpxy'):
            unlink('/etc/rc4.d/S20udpxy')
        else:
            symlink('/etc/init.d/udpxy', '/etc/rc4.d/S20udpxy')
        if path.exists('/etc/rc5.d/S20udpxy'):
            unlink('/etc/rc5.d/S20udpxy')
        else:
            symlink('/etc/init.d/udpxy', '/etc/rc5.d/S20udpxy')
        if path.exists('/etc/rc6.d/K20udpxy'):
            unlink('/etc/rc6.d/K20udpxy')
        else:
            symlink('/etc/init.d/udpxy', '/etc/rc6.d/K20udpxy')
        self.updateList()

    
    def updateList(self):
        import process
        p = process.ProcessList()
        udpxy_process = str(p.named('udpxy')).strip('[]')
        self['labrun'].hide()
        self['labstop'].hide()
        self['labactive'].hide()
        self['labdisabled'].hide()
        self.my_udpxy_active = False
        self.my_udpxy_run = False
        if path.exists('/etc/rc3.d/S20udpxy'):
            self['labdisabled'].hide()
            self['labactive'].show()
            self.my_udpxy_active = True
        else:
            self['labactive'].hide()
            self['labdisabled'].show()
        if udpxy_process:
            self.my_udpxy_run = True
        if self.my_udpxy_run == True:
            self['labstop'].hide()
            self['labrun'].show()
            self['key_yellow'].setText(_('Stop'))
        else:
            self['labstop'].show()
            self['labrun'].hide()
            self['key_yellow'].setText(_('Start'))
        self.list = []
        
    def quit(self):
        self.close()

    

class testcam(Screen):
    skin = '\n\t\t<screen position="center,center" size="590,400" title="Test Cam">\n\t\t\t<widget name="lab1" position="10,0" size="100,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labdisabled" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labactive" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2" />\n\t\t\t<widget name="lab2" position="240,0" size="150,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labstop" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labrun" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2"/>\n\t\t\t<widget source="list" render="Listbox" position="10,35" size="540,325" scrollbarMode="showOnDemand" >\n\t\t\t\t<convert type="StringList" />\n\t\t\t</widget>\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="150,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="300,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="450,350" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget name="key_yellow" position="150,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_green" position="300,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_blue" position="450,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
	Screen.__init__(self, session)
        Screen.setTitle(self, _('Test Cam'))
        self['labactive'] = Label(_(_('Active')))
        self['labdisabled'] = Label(_(_('Disabled')))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self.Console = Console()
        self.my_cam_active = False
        self.my_cam_run = False
        self['key_red'] = Label(_('ver log'))
        self['key_yellow'] = Label(_('Start'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'MenuActions'], {'back': self.close,
         'red': self.verlog,
         'yellow': self.camStart})
        self.onLayoutFinish.append(self.updateList)

    def camStart(self):
        if self.my_cam_run == False:
	    self.Console = Console()
            self.Console.ePopen('/etc/init.d/emutest start')
            self.Console.ePopen('killall -9 emutest')
            sleep(3)
            self.updateList()
        elif self.my_cam_run == True:
            self.session.open(SFConsole, title=_('Stop cam'), cmdlist=['/etc/init.d/emutest stop'])
            sleep(3)
            self.updateList()

     
    def updateList(self):
        import process
        p = process.ProcessList()
        cam_process = str(p.named('emutest.sh')).strip('[]')
        self.my_cam_active = False
        self.my_cam_run = False
        if cam_process:
            self.my_cam_run = True
        if self.my_cam_run == True:
            self['labstop'].hide()
            self['labrun'].show()
            self['key_yellow'].setText(_('Stop'))
        else:
            self['labstop'].show()
            self['labrun'].hide()
            self['key_yellow'].setText(_('Start'))
        self.list = []

    def verlog(self):
        self.session.open(SFConsole, title=_('Log Test Cam'), cmdlist=['cat /tmp/sfemutest.log'])

        
    def quit(self):
        self.close()


class testcard(Screen):
    skin = '\n\t\t<screen position="center,center" size="590,400" title="Test Card">\n\t\t\t<widget name="lab1" position="10,0" size="100,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labdisabled" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labactive" position="110,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2" />\n\t\t\t<widget name="lab2" position="240,0" size="150,24" font="Regular;20" valign="center" transparent="0" />\n\t\t\t<widget name="labstop" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="red" zPosition="1" />\n\t\t\t<widget name="labrun" position="390,0" size="100,24" font="Regular;20" valign="center" halign="center" backgroundColor="green" zPosition="2"/>\n\t\t\t<widget source="list" render="Listbox" position="10,35" size="540,325" scrollbarMode="showOnDemand" >\n\t\t\t\t<convert type="StringList" />\n\t\t\t</widget>\n\t\t\t<ePixmap pixmap="skin_default/buttons/red.png" position="0,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/yellow.png" position="150,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/green.png" position="300,350" size="140,40" alphatest="on" />\n\t\t\t<ePixmap pixmap="skin_default/buttons/blue.png" position="450,350" size="140,40" alphatest="on" />\n\t\t\t<widget name="key_red" position="0,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#9f1313" transparent="1" />\n\t\t\t<widget name="key_yellow" position="150,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_green" position="300,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t\t<widget name="key_blue" position="450,350" zPosition="1" size="140,40" font="Regular;20" halign="center" valign="center" backgroundColor="#a08500" transparent="1" />\n\t\t</screen>'

    def __init__(self, session):
	Screen.__init__(self, session)
        Screen.setTitle(self, _('Test Card'))
        self['labactive'] = Label(_(_('Active')))
        self['labdisabled'] = Label(_(_('Disabled')))
        self['lab2'] = Label(_('Current Status:'))
        self['labstop'] = Label(_('Stopped'))
        self['labrun'] = Label(_('Running'))
        self.Console = Console()
        self.my_cam_active = False
        self.my_cam_run = False
        self['key_red'] = Label(_('ver log'))
        self['key_yellow'] = Label(_('Start'))
        self.list = []
        self['list'] = List(self.list)
        self['actions'] = ActionMap(['WizardActions', 'ColorActions', 'MenuActions'], {'back': self.close,
         'red': self.verlog,
         'yellow': self.camStart})
        self.onLayoutFinish.append(self.updateList)

    def camStart(self):
        if self.my_cam_run == False:
	    self.Console = Console()
            self.Console.ePopen('/etc/init.d/cardtest start')
            self.Console.ePopen('killall -9 cardtest')
            sleep(3)
            self.updateList()
        elif self.my_cam_run == True:
            self.session.open(SFConsole, title=_('Stop cam'), cmdlist=['/etc/init.d/cardtest stop'])
            sleep(3)
            self.updateList()

    
    
    def updateList(self):
        import process
        p = process.ProcessList()
        cam_process = str(p.named('cardtest.sh')).strip('[]')
        self.my_cam_active = False
        self.my_cam_run = False
        if cam_process:
            self.my_cam_run = True
        if self.my_cam_run == True:
            self['labstop'].hide()
            self['labrun'].show()
            self['key_yellow'].setText(_('Stop'))
        else:
            self['labstop'].show()
            self['labrun'].hide()
            self['key_yellow'].setText(_('Start'))
        self.list = []

    def verlog(self):
        self.session.open(SFConsole, title=_('Log Test Card'), cmdlist=['cat /tmp/sfcardtest.log'])

        
    def quit(self):
        self.close()



