#!/usr/bin/python3
import datetime

def RecordError(msg):
	with open("error.log", "a") as f:
		f.writelines(["{0} {1}\n".format(datetime.datetime.now(), msg)])
