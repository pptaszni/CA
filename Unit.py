# Class for Unit

import xml.etree.ElementTree as ET
from ConnectionsAndParsing import SendMsg, ReceiveAndParse
from CommandInterpreter import InterpretResponse
from Field import Field
import logging


class Unit:

    def __init__(self, xml_unit):
        params = xml_unit.attrib
        self.action = params['action']
        self.hp = int(params['hp'])
        self.id = params['id']
        self.level = params['level']
        self.orientation = params['orientation']
        self.player = params['player']
        self.status = params['status']
        self.x = params['x']
        self.y = params['y']
        self.surroundings = {}

        sees_list = xml_unit.getchildren()
        self.UpdateSurroundings(sees_list)

    def UpdateSurroundings(self, surr):
        self.surroundings = {}
        for elem in surr:
            self.surroundings[elem.attrib['direction']] = Field(elem)
    def UpdatePosition(self, x, y, phi, hp):
        self.x = x
        self.y = y
        self.orientation = phi
        self.hp = int(hp)
    def Go(self, method, param, socket):
        if method == 'direction':
            if not param in ['E', 'SE', 'SW', 'W', 'NW', 'NE']:
                logging.error('Bad direction code '+param)
                param = 'E'
        elif method == 'rotate':
            if not param in ['rotateLeft','rotateRight']:
                logging.error('Bad rotation '+param)
                param='rotateLeft'
        elif method == 'action':
            if not param in ['drag','drop','heal','attack','hold']:
                logging.error('Bad action '+param)
                param='hold'
        else:
            logging.error('Unknown method '+method)
            method='action'
            param='hold'

        cmd = ET.Element('unit')
        cmd.set('id',self.id)
        ET.SubElement(cmd,'go')
        cmd.find('go').set(method,param)
        SendMsg(socket, ET.tostring(cmd))
        resp = ReceiveAndParse(socket)
        result = InterpretResponse(resp)
        if len(resp)>1 and result['end'] == False:
            for u in (x for x in resp[1].find('units').findall('unit') 
                    if x.attrib['id'] == self.id):
                self.UpdateSurroundings(u.getchildren())
                self.UpdatePosition(u.attrib['x'], u.attrib['y'], 
                        u.attrib['orientation'], u.attrib['hp'])
        logging.debug(self.surroundings)
        return {'result':result,'log':resp}

    def Move(self, direction, socket):
        return self.Go('direction',direction,socket)

    def Rotate(self, direction, socket):
        return self.Go('rotate',direction,socket)

    def Action(self, action, socket):
        return self.Go('action',action,socket)


def CreateUnitInstances(resp):
    game = resp[1]
    xmlUnits = game.find('units').findall('unit')
    units = [Unit(u) for u in xmlUnits]
    for u in units:
        logging.info('Unit '+u.id+' created')
    return units
