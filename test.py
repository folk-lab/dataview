#!/usr/bin/python3
import os
from smb.SMBConnection import SMBConnection

conn = SMBConnection(
	'galeky83', '####',			# Username, password
	'qdot-phys-36.physik.unibas.ch',	# Client machine
	'phys-jumbo.physik.unibas.ch',		# Server machine
	use_ntlm_v2 = True)
	
conn.connect('10.34.8.3')
print("Connected, I suppose!")
lst = conn.listPath('zum$', 'Measurement_Data')
for item in lst:
	print(item.isDirectory, item.isNormal, item.isReadOnly, item.filename)
conn.close()
