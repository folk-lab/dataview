import os
from config import config
from smb.SMBConnection import SMBConnection

class FileSystem:
	def __init__(self):
		self.protocol = config['FileServerProtocol']
		if self.protocol == 'samba':
			self.root = config['SambaRootDirectory']
			self.serviceName = config['SambaServiceName']
			self.conn = SMBConnection(
				config['SambaUsername'], config['SambaPassword'],
				'',	config['SambaUsername'], use_ntlm_v2 = True)
			self.conn.connect(config['SambaServerIP'])
		elif self.protocol == 'local':
			self.root = config['LocalRootDirectory']
		
		
	def ListSubDirs(self, d):
		result = []
		if self.protocol == 'samba':
			lst = self.conn.listPath(self.serviceName, '{0:s}/{1:s}'.format(self.root, d))
			for item in lst:
				if item.isDirectory and not item.filename in ['.', '..']:
					result.append(item.filename)
		elif self.protocol == 'local':
			lst = os.listdir(os.path.join(self.root, d))
			for item in lst:
				if os.path.isdir(os.path.join(self.root, d, item)):
					result.append(item + os.path.sep)
		return result
	
	def ListFiles(self, d):
		result = []
		if self.protocol == 'samba':
			lst = self.conn.listPath('zum$', '{0:s}/{1:s}'.format(self.root, d))
			for item in lst:
				if item.isDirectory and not item.filename in ['.', '..']:
					result.append(item.filename)
		elif self.protocol == 'local':
			lst = os.listdir(os.path.join(self.root, d))
			for item in lst:
				if os.path.isfile(os.path.join(self.root, d, item)):
					result.append(item)
		return result

			
