#!/usr/bin/env python

# Written by Dan Emmons for the DevOps API Challenge. Released to the public domain.

# Challenge: Write a script that clones a server (takes an image and deploys the
# image on a new server)

import os
import pyrax
import time
import datetime

pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))

#set variables
sourceServerUuid = raw_input("Enter UUID of server to clone: ")
sourceRegion = raw_input("Enter region (DFW for Dallas, ORD for Chicago) :") 
sourceServer = pyrax.connect_to_cloudservers(sourceRegion).servers.get(sourceServerUuid)
today = str(datetime.datetime.today())[:10]
print sourceServer # debug
print "Creating image of server %s (%s)" % (sourceServer.name, sourceServer.id)

# create image
sourceServer.create_image(sourceServer.name + "-forCloning-" + today)
# get image id
imageId = ""
while imageId == "":
	for i in pyrax.connect_to_cloudservers(sourceRegion).images.list():
		if sourceServer.name + "-forCloning-" + today in i.name:
			imageId = i.id
			# could 'break' here to match first occurrence, but actually want last / most recent, in case there are several
	time.sleep(1)
print "waiting for image to complete, this could take minutes or even hours for a"
print "server with a lot of used disk space."
print
lastProgress = 0
imageObj = pyrax.connect_to_cloudservers(sourceRegion).images.get(imageId)
while imageObj.progress != 100:
	if imageObj.progress > lastProgress:
		lastProgress = imageObj.progress
		if imageObj.progress == 25:
			print "Preparing image on Host machine"
		elif imageObj.progress == 50:
			print "Uploading image to Cloud Files"
		elif imageObj.progress > 51:
			print "Finishing up image process"
	#print imageObj.progress #debug
	time.sleep(1)
	imageObj = pyrax.connect_to_cloudservers(sourceRegion).images.get(imageId)
print "Image process complete. Creating clone server named %s..." % (sourceServer.name + "-clone-" + today,)
cloneServer = pyrax.connect_to_cloudservers(sourceRegion).servers.create(sourceServer.name + "-clone-" + today, imageObj.id, sourceServer.flavor["id"])
cloneId = cloneServer.id
cloneServerPassword = cloneServer.adminPass
time.sleep(1)
print "Server building. This will probably take longer than the image did."

cloneProgress = 0
while cloneServer.status != "ACTIVE":
	if cloneServer.status == "ERROR":
		print "Unfortunately, your build has gone into an error state."
		decision = ""
		while decision != "y" and decision != "n":
			decision = raw_input("Would you like to delete it and retry build? (y/n) ")
			if decision == "y":
				cloneServer.delete()
				print "Ok, failed clone server %s deleted." % (cloneServer,)
				print "retrying clone server creation (still named %s)..." % (sourceServer.name + "-clone-" + today,)
				cloneServer = pyrax.connect_to_cloudservers(sourceRegion).servers.create(sourceServer.name + "-clone-" + today, imageObj.id, sourceServer.flavor)
				cloneId = cloneServer.id
				cloneServerPassword = cloneServer.adminPass
				time.sleep(1)
				cloneProgress = 0
				while cloneServer.status != "ACTIVE":
        				if cloneServer.status == "ERROR":
                				print "Unfortunately, your build has gone into an error state again."
						print"It's probably best to retry from the start, with a new image."
						print"If this keeps happening, Rackspace Cloud Support should be able to help figure out why."
						exit(1)
					else:
						cloneServer = pyrax.connect_to_cloudservers(sourceRegion).servers.get(cloneId)
						if cloneServer.progress > cloneProgress:
							cloneProgress = cloneServer.progress
							print "Build Progress: %d percent complete" % (cloneProgress,)
						time.sleep(1)
			elif decision == "n":
				print "Ok, we'll just exit then. You can delete the failed build from your Cloud Control Panel and retry any time."
			else:
				print "You answered '%s'. I'm looking for a 'y' or a 'n' only." % (decision,)
	else:
		cloneServer = pyrax.connect_to_cloudservers(sourceRegion).servers.get(cloneId)
		if cloneServer.progress > cloneProgress:
			cloneProgress = cloneServer.progress
			print "Build Progress: %d percent complete" % (cloneProgress,)
		time.sleep(1)
	

#output credentials of new server, since we have them
print
print "Your clone server %s (%s) was completed successfully. Here are the credentials:" % (cloneServer.name, cloneServer.id)

if len(cloneServer.networks) >1:
	if len(cloneServer.networks["public"][0]) > 16: # we need to check whether this is IPv6, and I'm too lazy for a RegExp
		print "IPv4 Address: %s" % (cloneServer.networks["public"][1],)
		print "IPv6 Address: %s" % (cloneServer.networks["public"][0],)
	else:
		print "IPv4 Address: %s" % (cloneServer.networks["public"][0],)
		print "IPv6 Address: %s" % (cloneServer.networks["public"][1],)
print "Admin / root password: %s" % (cloneServerPassword,)
print

#last step is to clean up the image if desired.
decision = ""
while decision != "y" and decision != "n":
	decision = raw_input("Now that we're done, would you like to delete the '-forCloning' image we created? (y/n) ")
	if decision == "y":
		imageObj.delete()
		print "Ok, image cleaned up."
	elif decision == "n":
		print "Ok, keeping image named %s."
	else:
		print "You answered '%s'. I'm looking for a 'y' or a 'n' only." % (decision,)
print
print "All done!"
exit(0)

