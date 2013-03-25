#!/usr/bin/env python

# Written by Dan Emmons for the DevOps API Challenge. Released to the public domain.

# Challenge: Write a script that clones a server (takes an image and deploys the
# image on a new server)

import os
import pyrax
import time

pyrax.set_credential_file(os.path.expanduser("~/.rackspace_cloud_credentials"))

#set variables
