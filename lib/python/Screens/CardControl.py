import os

class CardControlService:
	'''CARDSERVER convention is that a softlink named /etc/init.c/cardserver.* points
	to the start/stop script.'''
	def __init__(self, name):
		self.name = name
		self.link = '/etc/init.d/' + name
		if not os.path.exists(self.link):
			print "[CardserverControl] No cardserver link?", self.link

	def getList(self):
		result = []
		prefix = self.name + '.'
		for f in os.listdir("/etc/init.d"):
			if f.startswith(prefix):
				result.append(f[len(prefix):])
		return result

	def current(self):
		try:
			l = os.readlink(self.link)
			return os.path.split(l)[1].split('.', 2)[1]
		except:
			pass
		return None

	def command(self, cmd):
		if os.path.exists(self.link):
			print "Executing", self.link + ' ' + cmd
			os.system(self.link + ' ' + cmd)

	def select(self, which):
		print "Selecting CARDSERVER:", which
		if not which:
			which = "None"
		dst = self.name + '.' + which
		if not os.path.exists('/etc/init.d/' + dst):
			print "[CardserverControl] init script does not exist:", dst
			return 
		try:
			os.unlink(self.link)
		except:
			pass
		try:
			os.symlink(dst, self.link);
		except:
			print "Failed to create symlink for cardserver:", dst
			import sys
			print sys.exc_info()[:2]

