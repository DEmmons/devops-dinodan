#!/usr/bin/env python

# Written by Dan Emmons for the DevOps API Challenge. Released to the public domain.

# Challenge: Write a script that builds three 512 MB Cloud Servers that follow
# a similar naming convention, and returns the IP and login credentials for
# each server. Use any image you want.

import os
import pyrax
import time

pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))

#set variables
newServersImage = "c195ef3b-9195-4474-b6f7-16e5bd86acd0" # CentOS 6.3
newServersFlavor = 2 # 512 MB
newServersAmount = 3 
newServersNameScheme = "challengeserver"
newServersNames = []

def hasAllIps():
	complete = True
	for i in range(newServersAmount):
		if newServers[i]["ipv4"] == "":
			complete = False
	return complete

for i in range(newServersAmount):
	newServersNames.append("%s-%d" % (newServersNameScheme, i+1))

def outputServers():
	for i in range(newServersAmount):
		print "Credentials for %s (ID: %s)" % (newServers[i]["name"], newServers[i]["id"])
		print "IPs: %s (IPv4), %s (IPv6)" % (newServers[i]["ipv4"], newServers[i]["ipv6"])
		print "Username: root (all lowercase)"
		print "Password: %s" % (newServers[i]["password"])
		print "Port: 22"
		print "Protocols enabled: SSH and SFTP"
		print

print "Creating %s Cloud Servers with the naming scheme: '%s-<number>'" % (newServersAmount, newServersNameScheme)

newServersObj = []
newServers = []

for servername in newServersNames:
	#create server and return object
	newServersObj.append(pyrax.cloudservers.servers.create(servername, newServersImage, newServersFlavor))
	#print  newServersObj
	thisDict = {}
	thisDict["name"] = newServersObj[-1].name
	thisDict["id"] = newServersObj[-1].id
	thisDict["password"] = newServersObj[-1].adminPass
	newServers.append(thisDict)
	time.sleep(5) #give it a moment

	newServers[-1]["ipv4"] = ""
	newServers[-1]["ipv6"] = ""
	print
	print "Server named %s created." % (thisDict["name"],)

print

print "Waiting for network provisioning. This could take up to 5 minutes..."
elapsed = 0	
while hasAllIps() == False:
	for i in range(newServersAmount):
		thisServer = pyrax.cloudservers.servers.get(newServers[i]["id"])
		# print thisServer.networks
		if newServers[i]["ipv4"] == "":
			if len(thisServer.networks) >=1:
				if len(thisServer.networks["public"][0]) > 16: # we need to check whether this is IPv6, and I'm too lazy for a RegExp
					newServers[i]["ipv4"] = thisServer.networks["public"][1]
					newServers[i]["ipv6"] = thisServer.networks["public"][0]
				else:
					newServers[i]["ipv4"] = thisServer.networks["public"][0]
					newServers[i]["ipv6"] = thisServer.networks["public"][1]
	if elapsed >= 300:
		print "It's been more than 5 minutes and we don't have IPs for at least one of your servers yet. Check the control panel for updates on those. This is what we have so far:"
		print
		outputServers()
		exit(1)
	else:
		time.sleep(1)
		elapsed += 1

print "All servers created successfully:"
print
outputServers()
exit(0)

