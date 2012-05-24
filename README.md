dataware.slibs
==============

add following code into settings.py in each project:

# add dataware shared libs in

import os

import sys

PROJECT_ROOT=os.path.dirname(__file__)

sys.path.insert(0, os.path.join(PROJECT_ROOT, '../../../../dataware.slibs/'))