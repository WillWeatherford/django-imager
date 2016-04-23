"""Overwrite and add settings specifically for production deployed instance."""
from imagersite.settings import *

DEBUG = False
ALLOWED_HOSTS.append('ec2-52-39-88-2.us-west-2.compute.amazonaws.com')
