# This module provides basic command interpretation engine.


# Returns: 
# -1 on error
#  id on response status == GAME_READY

import xml.etree.ElementTree as ET
import logging

def InterpretFirstResponse(resp):
        
    if resp[0].tag == 'error':
            print 'Error: Bad response'
            return -1
    elif resp[0].tag == 'response':
        print 'Server status: ' + resp[0].attrib['status']
        if resp[0].attrib['status'] == 'GAME_READY':
            game_id = resp[0].find('game').attrib['id']
            print 'Game ready, game_id = ' + game_id
    else:
        print 'Unknown response: ' + resp.tag
        return -1

    return game_id

def InterpretResponse(resp):

    succes = False
    end = False
    if resp[0].tag == 'ok':
        succes = True
        # Code for interpreting the scene state here
    elif resp[0].tag == 'error':
        logging.error(resp[0].attrib['description'])
    else:
        logging.error('Unknown response: ' + resp[0].tag)
    if len(resp) == 2 and resp[1].attrib.has_key('result'):
        logging.debug("InterpResponse: " + str(resp))
        return {'succes':False,'end':True}
    return {'succes':succes,'end':end}
