# -*- coding: utf-8 -*-

import os
from config import config

class FileSystem:
	def __init__(self):
		self.protocol = config['FileServerProtocol']
		if self.protocol == 'samba':
			try:
				from smb.SMBConnection import SMBConnection
			except ImportError:
				raise ImportError('Cannot serve data from Samba share. pysmb not installed.')
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
				if (item.isDirectory) and not (item.filename in ['.', '..']):
					result.append(item.filename)
		elif self.protocol == 'local':
			lst = os.listdir(os.path.join(self.root, d[:-1]))
			for item in lst:
				item_path = os.path.join(self.root, d[:-1], item)
				if os.path.isdir(item_path) \
				  and not (os.path.basename(item_path).startswith('.')) \
				  and not (os.path.basename(item_path).startswith('__')):
					result.append(item + os.path.sep)
		return result

	def ListFiles(self, d):

		result = []
		displayed_types = ['.h5', '.hdf5', '.ibw', '.png', '.jpg', '.jpeg']

		if self.protocol == 'samba':
			lst = self.conn.listPath('zum$', '{0:s}/{1:s}'.format(self.root, d))
			for item in lst:
				if item.isDirectory and not item.filename in ['.', '..']:
					result.append(item.filename)
		elif self.protocol == 'local':
			lst = os.listdir(os.path.join(self.root, d))
			for item in lst:
				item_path = os.path.join(self.root, d, item)
				_, item_type = os.path.splitext(item_path)
				if ( os.path.isfile(item_path) ) and ( item_type in displayed_types ):
					result.append(item_path)
		return [os.path.basename(p)
					for p in sorted(result, key = os.path.getmtime, reverse=True)]

	def IsPlottable(self, path):
		plottable_types = ['.h5', '.hdf5']
		_, item_type = os.path.splitext(path)
		if (self.protocol == 'local') and (os.path.isfile(os.path.join(self.root, path))) \
		 and (item_type in plottable_types):
			return True
		else:
			return False

	def FullPath(self, path):
		if self.protocol == 'local':
			return os.path.join(self.root, path)
		elif self.protocol == 'samba':
			raise NotImplementedError('Serving data from Samba shares not yet supported')
