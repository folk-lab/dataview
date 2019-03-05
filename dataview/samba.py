from config import config
from smb.SMBConnection import SMBConnection

class Samba:
	def __init__(self):
		self.root = config['SambaRootDirectory']
		self.conn = SMBConnection(
			config['SambaUsername'], config['SambaPassword'],
			'',	config['SambaUsername'], use_ntlm_v2 = True)
		self.conn.connect(config['SambaServerIP'])
	def ListSubDirs(self, d):
		result = []
		lst = self.conn.listPath('zum$', '{0:s}/{1:s}'.format(self.root, d))
		for item in lst:
			if item.isDirectory and not item.filename in ['.', '..']:
				result.append(item.filename)
		print(d, result)
		return result
	def ListFiles(self, d):
		return []
	def DirName(self, d):
		return ''
	def DownloadFile(self, fn):
		return None
