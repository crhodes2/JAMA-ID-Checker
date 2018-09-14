# !/usr/bin/env python3
# -*- mode: python -*-

##############################
''' BUILD URL '''
##############################

# LIST OF MODULES #########################################################################


#    VARIABLES    #########################################################################

id = ''


#    FUNCTIONS    #########################################################################

def templateURL(id):
    url='https://www.jamaland.com/rest/latest/abstractitems?documentKey={0}'. format(id)
    return url