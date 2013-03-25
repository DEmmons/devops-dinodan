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
