#!/usr/bin/env python

# Written by Dan Emmons for the DevOps API Challenge. Released to the public domain.

# Challenge: Write a script that uses Cloud DNS to create a
# new A record when passed a FQDN and IP address as arguments.

import os
import pyrax
import time
import string

pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))

def zoneFound(zone):
	found=False
	zoneObjs = pyrax.cloud_dns.list()
	for i in zoneObjs:
		if i.name == zone:
			found = True
			zoneObj = i
	return found
#set variables
zoneObj = pyrax.cloud_dns.list()[0]
print "This script adds a new A record to an existing domain set up in the Rackspace Cloud DNS."
isFqdn = False
while isFqdn == False:
	fqdn = raw_input("Enter the Fully Qualified Domain Name to add the record for: ")
	try:
		isFqdn = True
		fqdnsplit = string.split(fqdn,".")
		zone = string.lower(fqdnsplit[-2]) + "." + string.lower(fqdnsplit[-1])
	except IndexError:
		print "This is not a valid domain. Try again."
		isFqdn = False
#print fqdn, fqdnsplit, zone #debug
#print pyrax.cloud_dns.list() # debug

while zoneFound(zone) == False:
	print "Root Domain %s not found in this account, so FQDN %s cannot be added. You can only add a record that would be part of an existing domain." % (zone, fqdn)
	isFqdn = False
	while isFqdn == False:
        	fqdn = raw_input("Enter the Fully Qualified Domain Name to add the record for: ")
        	try:
                	isFqdn = True
                	fqdnsplit = string.split(fqdn,".")
			zone = string.lower(fqdnsplit[-2]) + "." + string.lower(fqdnsplit[-1])
        	except IndexError:
                	print "This is not a valid domain. Try again."
                	isFqdn = False
ip = raw_input("Enter the IP this new record should resolve to: ")
print "Creating A record for %s (root domain: %s) that resolves to the IP Address: %s" % (fqdn, zone, ip)
newRecord = {}
newRecord["type"] = "A"
newRecord["name"] = fqdn
newRecord["data"] = ip
try:
	result = pyrax.cloud_dns.add_records(zoneObj, newRecord)
	#print result #debug
except pyrax.exceptions.OverLimit:
	print "an over-limit warning was raised by the API, but the record should still appear in a moment."
	print "done!"
	exit(1)
if result[0].name == fqdn:
	print "A record successfully created."
	print "done!"
	exit(0)
else:
	print "an error occurred, check whether zone created and if not, try again."
	print "done!"
	exit(1)
