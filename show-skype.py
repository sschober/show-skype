#!/usr/bin/env python
# -*- coding: iso-8859-15 -*-

import dbus, sys, getopt

def main(argv):
	# option handling inspired by:
	# http://www.faqs.org/docs/diveintopython/kgp_commandline.html
	_debug = 1
	try:
	  opts, args = getopt.getopt(argv, "d", ["debug"])
	except getopt.GetoptError:
	  sys.exit("Unkown option")
	for opt, arg in opts:
	  if opt in ("-d", "--debug"):
	    _debug = 1
	  else:
	    print "? ", opt

	skype_api_found = 0
	bus = dbus.SessionBus()
	if not bus:
	  sys.exit("No session bus found.")

	proxy = bus.get_object('org.freedesktop.DBus', '/org/freedesktop/DBus')
	if not proxy:
	  sys.exit("Couldn't acquire proxy.")

	service_list = proxy.ListNames()
	for service in service_list:
	  if _debug:
	    print service
	  if service=='com.Skype.API':
	    skype_api_found = 1
	    break

	if not skype_api_found:
	  sys.exit('No running API-capable Skype found')

	skype_proxy = bus.get_object('com.Skype.API', '/com/Skype')
	answer = skype_proxy.Invoke('NAME SkypeApiPythonTestClient')
	if answer != 'OK':
	  sys.exit('Could not bind to Skype client')

	answer = skype_proxy.Invoke('PROTOCOL 1')
	if answer != 'PROTOCOL 1':
	  sys.exit('This test program only supports Skype API protocol version 1')
	answer = skype_proxy.Invoke('SET WINDOWSTATE NORMAL')
	print answer
	return 0

if __name__ == "__main__":
	main(sys.argv)

