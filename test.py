#!/usr/bin/python3
import os

rootDir = '/home/msamani/Academia/Basel/ViewMeasurements'
string = ""

def PrintSubDir(curDir, string):
	string += "<li>{0:s}".format(os.path.basename(curDir))
	string += "<ul>"
	for subDir in os.listdir(curDir):
		if os.path.isdir(os.path.join(curDir, subDir)) and not subDir.startswith('.'):

			hasSubs = True
			string = PrintSubDir(os.path.join(curDir, subDir), string)
	
	string += "</ul>"
	string += "</li>"
	return string

string += "<ul>"
string = PrintSubDir(rootDir, string)
string += "</ul>"

print(string)
