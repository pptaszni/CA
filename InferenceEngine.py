# Inference engine

# This module provides human-like reasoning functionalities. It controls the units and reads the map in order to make decisions about units movement and actions that will lead to win.


import clips
import random
import logging
import pickle
from AStar import AStar


class InferenceEngine:
    def __init__(self, units, _map, socket):
        self.units = units
        self._map = _map
        self.s = socket
    def Start(self):
        self.ExploreAndReturn()
    def ExploreAndReturn(self):
        random.seed()
        u = self.units[0]
        m = self._map
        resp = ''
        result = u.Action('hold',self.s)['result']
        startPoint = (int(u.x),int(u.y))
        while u.hp > 50:
            availableDirs = []
            for key, value in u.surroundings.iteritems():
                if value.movable:
                    availableDirs.append(key)
                    if key in ['E','NE','SE']:
                        availableDirs.append(key)
            upper = len(availableDirs)
            d = random.randint(0,upper-1)
            resp = u.Move(availableDirs[d],self.s)
            result = resp['result']
            m.UpdateMap(u.x, u.y, u.surroundings)
        while (int(u.x),int(u.y)) != startPoint:
            path = AStar(m,(int(u.x),int(u.y)),startPoint).Start()
            if path['status'] == 'OK':
                logging.debug(str(path))
                resp = u.Move(path['direction'],self.s)
                m.UpdateMap(u.x, u.y, u.surroundings)
        while result['end'] == False:
            resp = u.Action('hold',self.s)
            result = resp['result']
            m.UpdateMap(u.x, u.y, u.surroundings)
        print str(resp['log'][1].__dict__)
 
    def Explore(self):
        random.seed()
        u = self.units[0]
        m = self._map
        resp = ''
        result = u.Action('hold',self.s)['result']
        while result['end'] == False:
            availableDirs = []
            for key, value in u.surroundings.iteritems():
                if value.movable:
                    availableDirs.append(key)
            upper = len(availableDirs)
            d = random.randint(0,upper-1)
            resp = u.Move(availableDirs[d],self.s)
            result = resp['result']
            m.UpdateMap(u.x, u.y, u.surroundings)
        print str(resp['log'][1].__dict__)
        logging.debug(str(m.__dict__))
        #fileObj = open('map.dat','wb')
        #pickle.dump(m,fileObj)
        #fileObj.close()
