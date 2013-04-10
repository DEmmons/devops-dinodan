#!/usr/bin/env python

# Written by Dan Emmons for the DevOps API Challenge. Released to the public domain.

# Challenge: Write a script that accepts a directory as an argument as well as a
# container name. The script should upload the contents of the specified directory
# to the container (or create it if it doesn't exist). The script should handle
# errors appropriately

import os
import pyrax
import time

pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))

#set variables

sourceDir = raw_input("Enter path to the directory / folder to be uploaded: ")
destContainer = raw_input("Enter name of container to upload to (will be created if it does not already exist): ")
destRegion = raw_input("Enter Cloud Files region (DFW for Dallas, ORD for Chicago): ")
while destRegion != "DFW" and destRegion != "ORD":
	destRegion = raw_input("Enter Cloud Files region (DFW for Dallas, ORD for Chicago): ")

cfEndpoint = pyrax.connect_to_cloudfiles(destRegion)

print cfEndpoint.list_containers() #debug
if destContainer in cfEndpoint.list_containers():
	print "A container named %s exists in region %s, using it." % (destContainer, destRegion)
else:
	print "No container named %s found in region %s, creating it." % (destContainer, destRegion)
	cfEndpoint.create_container(destContainer)

destContainerObj = cfEndpoint.get_container(destContainer)
uploadTuple = cfEndpoint.upload_folder(sourceDir, destContainer)
print "Uploading all contents of %s to container %s, total upload size is %d bytes" % (sourceDir, destContainer, uploadTuple[1])
progress = 0
while cfEndpoint.get_uploaded(uploadTuple[0]) < uploadTuple[1]:
	if cfEndpoint.get_uploaded(uploadTuple[0]) > progress:
		progress = cfEndpoint.get_uploaded(uploadTuple[0])
		print "%d bytes uploaded (%d percent)" % (progress, float(progress) / (float(uploadTuple[1]) / 100.0) )
	time.sleep(1)

print "Upload Complete!"
