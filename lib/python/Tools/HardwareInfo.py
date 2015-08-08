from Tools.Directories import SCOPE_SKIN, resolveFilename

hw_info = None

class HardwareInfo:
	device_name = _("unavailable")
	device_model = None
	device_type = None
	device_version = ""
	device_revision = ""
	device_hdmi = False

	def __init__(self):
                global hw_info
		if hw_info is not None:
			return
		hw_info = self

		print "[HardwareInfo] Scanning hardware info"
		# Version
		try:
			self.device_version = open("/proc/stb/info/version").read().strip()
		except:
			pass

		# Revision
		try:
			self.device_revision = open("/proc/stb/info/board_revision").read().strip()
		except:
			pass

		# Name ... bit odd, but history prevails
		try:
			self.device_name = open("/proc/stb/info/model").read().strip()
		except:
			pass

		# Model
		try:
			self.device_model = open("/proc/stb/info/model").read().strip()
		except:
			pass
			
		# Type
		try:
			self.device_type = open("/proc/stb/info/boxtype").read().strip()
		except:
			pass

		if self.device_model is None:
			self.device_model = self.device_name

		# HDMI capbility
		self.device_hdmi = (	self.device_name == 'gbx1' or
					self.device_name == 'gb800solo' or
					self.device_name == 'gb800se' or
					self.device_name == 'gb800ue' or
					self.device_name == 'gb800seplus' or
					self.device_name == 'gb800ueplus' or
					self.device_name == 'gbipbox' or
					self.device_name == 'gbultra' or
					self.device_name == 'gbultraue' or
					self.device_name == 'gbultrase' or
					self.device_name == 'gbquad' or
					self.device_name == 'gbquadplus' or
					self.device_name == 'tomcat' or
					self.device_name == 'quadbox2400' or
					self.device_name == 'dm800se' or
					self.device_name == 'dm500hd' or
					self.device_name == 'dm7020hd' or
					(self.device_name == 'dm8000' and self.device_version != None))

		print "Detected: " + self.get_device_string()


	def get_device_name(self):
		return hw_info.device_name

	def get_device_model(self):
		return hw_info.device_model
		
	def get_device_type(self):
		return hw_info.device_type
		
	def get_device_version(self):
		return hw_info.device_version

	def get_device_revision(self):
		return hw_info.device_revision

	def get_device_string(self):
		s = hw_info.device_model
		if hw_info.device_revision != "":
			s += " (" + hw_info.device_revision + "-" + hw_info.device_version + ")"
		elif hw_info.device_version != "":
			s += " (" + hw_info.device_version + ")"
		return s

	def has_hdmi(self):
		return hw_info.device_hdmi