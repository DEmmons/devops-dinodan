#!/usr/bin/env python

# Written by Dan Emmons for the DevOps API Challenge. Released to the public domain.

# Challenge: Write a script that creates a Cloud Database instance. This instance
# should contain at least one database, and the database should have at least one
# user that can connect to it.

import os
import pyrax
import time
import getpass

pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))

#set variables
dbName= ""
while len(dbName) < 1:
	dbName = raw_input("Enter a name for your new Cloud Database: ")

dbRegion = ""
while dbRegion != "DFW" and dbRegion != "ORD":
	dbRegion = raw_input("Enter the region you want the Cloud Database instance built in (DFW or ORD): ")
dbFlavor = 1
dbVolume = 1

dbEndpoint = pyrax.connect_to_cloud_databases(dbRegion)
newDb = dbEndpoint.create(dbName, dbFlavor, dbVolume)
time.sleep(2)
newDbId = ""
while newDbId == "":
	for i in dbEndpoint.list():
		if i.name == dbName:
			newDbId = i.id
			# could 'break' here to match first occurrence, but actually want last / most recent, in case there are several
	time.sleep(1)
newDb = dbEndpoint.get(newDbId)
print "Waiting for new Cloud Database instance to finish building, this may take a few minutes..."
while newDb.status != "ACTIVE":
	if newDb.status == "ERROR":
		print "Unfortunately, your build has gone into an error state."
		print "If it cannot be deleted from the Control Panel, contact Rackspace Cloud Support"
		print "done."
		exit (1)
	else:
		newDb = dbEndpoint.get(newDbId)
		
		time.sleep(1)

print "Build complete! time to create a MySQL Database and user"
databaseName = ""
while databaseName == "":
	databaseName = raw_input("Enter name for MySQL Database: ")
database = newDb.create_database(databaseName)

print "To access the Database, you'll also need a MySQL user."
userName = ""
while userName == "":
	userName = raw_input("Enter username for MySQL user: ")
passMatch = False
while passMatch == False:
	userPass = ""
	confirmPass = ""
	userPass = getpass.getpass(prompt='Enter Password for MySQL user: ')
	confirmPass = getpass.getpass(prompt='Confirm Password: ')
	if userPass == confirmPass and len(userPass) > 7:
		passMatch = True
	else:
		if userPass != confirmPass:
			print "Password mismatch"
		if len(userPass) < 8:
			print "Password should be at least 8 characters long"

newUser = newDb.create_user(userName, userPass, [databaseName])
print
print "Your Cloud Database Instance is now ready for use!"
print "Cloud Database Instance name:", newDb.name
print "Region:", dbRegion
print "MySQL Database name:", databaseName
print "MySQL User:", userName
print
print "All Done!"
exit(0)
