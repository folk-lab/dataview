import os
import logging
_fs_logger = logging.getLogger('dataview.filesystem')
from dataview import config

class FileSystem:
	def __init__(self):
		self.root = config['LocalRootDirectory']

	def GetDirName(self, d):
		if os.path.isfile(os.path.join(self.root, d)):
			return os.path.dirname(d)
		else:
			return d
			
	def GetParentDir(self, d):
		if os.path.isfile(os.path.join(self.root, d)):
			return os.path.normpath(os.path.join(os.path.dirname(d), os.pardir))
		else:
			return os.path.normpath(os.path.join(d, os.pardir))
			
	def ListSubDirs(self, d):
		result = []
		if os.path.isfile(os.path.join(self.root, d)):
			d = os.path.dirname(d)
		lst = os.listdir(os.path.join(self.root, d))
		_fs_logger.debug(f'ListSubDirs {lst}')
		for item in lst:
			item_path = os.path.join(self.root, d, item)
			if os.path.isdir(item_path) \
			  and not (os.path.basename(item_path).startswith('.')) \
			  and not (os.path.basename(item_path).startswith('__')) \
			  and not (os.path.basename(item_path).startswith('config')):
				result.append(os.path.join(d, item))
		return result

	def ListFiles(self, d):
		result = []
		displayed_types = config['DisplayableTypes']
		if os.path.isfile(os.path.join(self.root, d)):
			d = os.path.dirname(d)
		
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
		if (os.path.isfile(os.path.join(self.root, path))) and (item_type in plottable_types):
			return True
		else:
			return False

	def FullPath(self, path):
		return os.path.join(self.root, path)
