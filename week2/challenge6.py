#!/usr/bin/env python

# Written by Dan Emmons for the DevOps API Challenge. Released to the public domain.

# Challenge: Write a script that creates a CDN-enabled container in Cloud Files.

import os
import pyrax
import time

pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))

#set variables

newContainer = raw_input("Enter name of the new container to create and enable CDN on: ")
destRegion = raw_input("Enter Cloud Files region (DFW for Dallas, ORD for Chicago): ")
while destRegion != "DFW" and destRegion != "ORD":
	destRegion = raw_input("Enter Cloud Files region (DFW for Dallas, ORD for Chicago): ")

cfEndpoint = pyrax.connect_to_cloudfiles(destRegion)

#print cfEndpoint.list_containers() #debug
if newContainer in cfEndpoint.list_containers():
	print "A container named %s exists in region %s, exiting without making changes" % (newContainer, destRegion)
	exit (1)
else:
	print "No pre-existing container named %s in region %s, so it's safe to create it. Creating now." % (newContainer, destRegion)
	cfEndpoint.create_container(newContainer)

newContainerObj = cfEndpoint.get_container(newContainer)
newContainerObj.make_public(ttl=9001)
time.sleep(1)
newContainerObj = cfEndpoint.get_container(newContainer)
cdnUri = newContainerObj.cdn_uri
print "Your new CDN-Enabled container has been created. The public URL for this container is:"
print cdnUri
print
print "Done!"
