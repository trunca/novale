	# -*- coding: utf-8 -*-
from Screen import Screen
from Components.Label import Label
from Components.MenuList import MenuList
from Components.ActionMap import ActionMap
from Plugins.Plugin import PluginDescriptor
from Tools.LoadPixmap import LoadPixmap
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Console import SFConsole
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import gettext
from Components.Language import language
from os import environ

class mainSFPanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="SF Panel v1.0">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('SF Panel v1.0')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Softcam configuration'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Backup configuration'), 'fileoperations.png'))
        l.append(self.buildListEntry(_('Multimedia configuration'), 'encoding.png'))
        l.append(self.buildListEntry(_('EPG configuration'), 'linkepg.png'))
        l.append(self.buildListEntry(_('Drivers configuration'), 'linkepg.png'))
        l.append(self.buildListEntry(_('Utilities'), 'zaperror.png'))
        l.append(self.buildListEntry(_('Updates'), 'filter.png'))
        l.append(self.buildListEntry(_('Information'), 'filter.png'))


        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			self.session.open(SoftcamPanel)
        elif menuIndex == 1:
            self.session.open(Backup)
        elif menuIndex == 2:
            self.session.open(multimedia)
        elif menuIndex == 3:
			import SFepg
			self.session.open(SFepg.CrossEPG_SFMenu)
        elif menuIndex == 4:
            self.session.open(drivers)
        elif menuIndex == 5:
            self.session.open(Utilities)
        elif menuIndex == 6:
			import Update
			self.session.open(Update.UpdatePanel)
        elif menuIndex == 7:
            self.session.open(infopanel)


    def quit(self):
        self.close()


class SoftcamPanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Softcam Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Softcam Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Configure softcam'), 'fileoperations.png'))
        l.append(self.buildListEntry(_('Configure cardserver'), 'filter.png'))

        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			import SoftPanel
			self.session.open(SoftPanel.SoftcamSetupSF)
        elif menuIndex == 1:
			import CardPanel
			self.session.open(CardPanel.CardserverSetup)

    def quit(self):
        self.close()


class Backup(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Backup Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Backup Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Backup to USB'), 'fileoperations.png'))

        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			import Backup
			self.session.open(Backup.BackupPanel)
        elif menuIndex == 1:
       		 self.close(False)

    def quit(self):
        self.close()

class SoftcamPanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Softcam Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Softcam Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Configure softcam'), 'fileoperations.png'))
        l.append(self.buildListEntry(_('Configure cardserver'), 'filter.png'))

        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			import SoftPanel
			self.session.open(SoftPanel.SoftcamSetupSF)
        elif menuIndex == 1:
			import CardPanel
			self.session.open(CardPanel.CardserverSetup)

    def quit(self):
        self.close()


class multimedia(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Multimedia Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Multimedia Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Configure Mediatomb'), 'fileoperations.png'))
        l.append(self.buildListEntry(_('Configure Tunerserver'), 'filter.png'))

        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
            import Mediatomb
            self.session.open(Mediatomb.MediatombPanel)
        elif menuIndex == 1:
            self.session.open(TunerPanel)

    def quit(self):
        self.close()

class TunerPanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Tunerserver Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Tunerserver Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Create channel list'), 'encoding.png'))


        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			import Tuner
			self.session.open(Tuner.TunerServer)

    def quit(self):
        self.close()	
		
class Utilities(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Utilities Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Utilities Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Mount Manager'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Cron Manager'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Root password changer'), 'encoding.png'))
        l.append(self.buildListEntry(_('Internet speed test'), 'copyepg.png'))

        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			import Mount
			self.session.open(Mount.HddMount)
        elif menuIndex == 1:
			import Cron
			self.session.open(Cron.CronManager)
        elif menuIndex == 2:
			import Password
			self.session.open(Password.PasswordChanger)
        elif menuIndex == 3:
			self.session.open(SFConsole,title = _("Running internet speed test"), cmdlist = ["python /usr/lib/enigma2/python/Screens/SpeedTest.pyo"])


    def quit(self):
        self.close()

class infopanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Information Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Information Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Check memory usage'), 'copyepg.png'))
        l.append(self.buildListEntry(_('Clean memory'), 'fileoperations.png'))
        l.append(self.buildListEntry(_('Proc information'), 'filter.png'))
        l.append(self.buildListEntry(_('Ecm information'), 'encoding.png'))
        l.append(self.buildListEntry(_('Driver version'), 'linkepg.png'))
        l.append(self.buildListEntry(_('Box uptime'), 'zaperror.png'))

        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			self.session.open(SFConsole,title = _("Check memory usage"), cmdlist = ["cat /proc/meminfo"])
        elif menuIndex == 1:
			self.session.open(SFConsole,title = _("Clean memory"), cmdlist = ["sync ; echo 3 > /proc/sys/vm/drop_caches"])
        elif menuIndex == 2:
			self.session.open(SFConsole,title = _("Proc information"), cmdlist = ["cat /proc/stb/info/boxtype & cat /proc/stb/info/gbmodel & cat /proc/stb/info/model & cat /proc/stb/info/chipset & cat /proc/stb/info/version"])
        elif menuIndex == 3:
			self.session.open(SFConsole,title = _("Ecm information"), cmdlist = ["cat /tmp/ecm.info"])
        elif menuIndex == 4:
			self.session.open(SFConsole,title = _("Driver version"), cmdlist = ["opkg list-installed | grep dvb-mod"])
        elif menuIndex == 5:
			self.session.open(SFConsole,title = _("Box uptime"), cmdlist = ["uptime"])

    def quit(self):
        self.close()

class drivers(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Drivers Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Drivers Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Configure TDT drivers'), 'fileoperations.png'))
        l.append(self.buildListEntry(_('Configure Wireless drivers'), 'filter.png'))

        self['list'] = List(l)
        self['setupActions'] = ActionMap(['SetupActions'], {'cancel': self.quit,
         'ok': self.openSelected}, -2)

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
            import Mediatomb
            self.session.open(tdtpanel)
        elif menuIndex == 1:
            self.session.open(wifipanel)

    def quit(self):
        self.close()

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

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			self.session.open(SFConsole,title = _("Installing drivers"), cmdlist = ["opkg install enigma2-plugin-drivers-dvb-usb-siano"])
        elif menuIndex == 1:
			self.session.open(SFConsole,title = _("Installing drivers"), cmdlist = ["opkg install enigma2-plugin-drivers-dvb-usb-af9015"])
        elif menuIndex == 2:
			self.session.open(SFConsole,title = _("Installing drivers"), cmdlist = ["opkg install enigma2-plugin-drivers-dvb-usb-af9035"])

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

    def buildListEntry(self, description, image):
        pixmap = LoadPixmap(cached=True, path='/usr/share/enigma2/sfpanel/%s' % image)
        return (pixmap, description)

    def openSelected(self):
        global menuIndex
        menuIndex = self['list'].getIndex()
        if menuIndex == 0:
			self.session.open(SFConsole,title = _("Installing drivers"), cmdlist = ["opkg install kernel-module-rtl8192cu firmware-rtl8192cu"])
        elif menuIndex == 1:
			self.session.open(SFConsole,title = _("Installing drivers"), cmdlist = ["opkg install kernel-module-rt2800usb"])
        elif menuIndex == 2:
			self.session.open(SFConsole,title = _("Installing drivers"), cmdlist = ["opkg install kernel-module-rt2500usb"])
        elif menuIndex == 3:
			self.session.open(SFConsole,title = _("Installing drivers"), cmdlist = ["opkg install kernel-module-rt73usb firmware-rt73"])

    def quit(self):
        self.close()

	









