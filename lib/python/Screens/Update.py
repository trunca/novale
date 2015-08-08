# -*- coding: utf-8 -*-
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
from SFtoolbox import getBoxType, getImageDistro, getMachineBrand, getMachineName

class UpdatePanel(Screen):
    skin = '\n\t<screen position="center,center" size="560,450" title="Update Panel">\n\t\t<widget source="list" render="Listbox" position="0,10" size="560,450" scrollbarMode="showOnDemand">\n\t\t\t<convert type="TemplatedMultiContent">\n\t\t\t\t{"template": [\n\t\t\t\t\tMultiContentEntryPixmapAlphaTest(pos = (12, 4), size = (32, 32), png = 0),\n\t\t\t\t\tMultiContentEntryText(pos = (58, 5), size = (440, 38), font=0, flags = RT_HALIGN_LEFT|RT_VALIGN_TOP, text = 1),\n\t\t\t\t\t],\n\t\t\t\t\t"fonts": [gFont("Regular", 22)],\n\t\t\t\t\t"itemHeight": 40\n\t\t\t\t}\n\t\t\t</convert>\n\t\t</widget>\t\n\t</screen>'


    def __init__(self, session, args = 0):
        self.session = session
        self.setup_title = _('Update Panel')
        Screen.__init__(self, session)
        l = []
        l.append(self.buildListEntry(_('Update image'), 'copyepg.png'))



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
			from Flash import FlashOnline
			self.session.open(FlashOnline)
  

    def quit(self):
        self.close()	
	