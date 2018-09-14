# !/usr/bin/env python3
# -*- mode: python -*-

##############################
''' RUN PROG '''
##############################

# LIST OF MODULES #########################################################################

import logging, time
import sys


#    VARIABLES    #########################################################################

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter()

commit_list_set = logging.StreamHandler(sys.stdout)

#    FUNCTIONS    #########################################################################

logger.addHandler(commit_list_set)


def start():

    print("\n")
    print('============================================================')
    print('    Please wait. This may take a few seconds... ')
    print('    Application is collecting information on GitHub Pull Request... ...')
    print('============================================================')
    time.sleep(2)
    time.sleep(2)


def closed():

    print("\n")
    print("\n")
    print('============================================================')
    print('                    !!!        ATTENTION       !!!                     \n'
          '                 THIS PULL REQUEST HAS BEEN CLOSED')
    print('    Please re-open this Pull Request again or create a new one to run the app.')
    print('============================================================')
    time.sleep(2)
