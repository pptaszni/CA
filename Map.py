# Map module. Provides set of fields with its coordinates and objects.

import logging

class Map:
    def __init__(self,x,y,fields):
        self.mapTuned = False
        # when TRUE, even numbered rows are shifted left, after each move in
        # direction NE or SE from this row x remains unchanged
        # after aceh move in direction NE or SE from odd numbered row
        # x augments
        self.EvenYShiftedLeft = True
        y = int(y)
        x = int(x)
        self.yBorder = y
        self.xBorder = x
        self._map = [None for i in range(0,y+1)]
        for i in range(0, len(self._map)):
            self._map[i] = [None for j in range(0,x+1)]
        self.UpdateMap(x,y,fields)
    def MapOffset(self,yEven,direction):
        shift = self.EvenYShiftedLeft
        if direction == 'E':
            xoff = 1
            yoff = 0
        elif direction == 'SE':
            xoff = int(yEven != shift)*1
            yoff = 1
        elif direction == 'SW':
            xoff = int(yEven == shift)*(-1)
            yoff = 1
        elif direction == 'W':
            xoff = -1
            yoff = 0
        elif direction == 'NW':
            xoff = int(yEven == shift)*(-1)
            yoff = -1
        elif direction == 'NE':
            xoff = int(yEven != shift)*1
            yoff = -1
        else:
            logging.error('Unsuspected offset direction: '+direction)
            xoff = 0
            yoff = 0
        return (xoff,yoff)
    def UpdateMap(self,x,y,fields):
        y = int(y)
        x = int(x)
        yEven = not bool(y%2)
        changedCoord = []
        if self.yBorder <= y:
            extRows = [[None for i in range(0,self.xBorder+1)]
                    for j in range(0,y-self.yBorder+1)]
            self._map.extend(extRows)
            self.yBorder = y+1
        if self.xBorder <= x:
            extCols = [None for i in range(0,x-self.xBorder+1)]
            for l in self._map:
                l.extend(extCols)
                self.xBorder = x+1
        for key,value in fields.iteritems():
            offset = self.MapOffset(yEven,key)
            if (x+offset[0] >= 0 and y+offset[1] >= 0):
                if value != self._map[y+offset[1]][x+offset[0]]:
                    self._map[y+offset[1]][x+offset[0]] = value
                    changedCoord.append((x+offset[0],y+offset[1]))
        return changedCoord
    def GetNeighbours(self,coords):
        y = int(coords[1])
        x = int(coords[0])
        yEven = not bool(y%2)
        neighbours = []
        for d in ['E','SE','SW','W','NW','NE']:
            offset = self.MapOffset(yEven,d)
            if (x+offset[0] >= 0 and y+offset[1] >= 0 and 
                    x+offset[0] < self.xBorder and
                    y+offset[1] < self.yBorder):
                neighbours.append({'coords':(x+offset[0],y+offset[1]),
                    'field':self._map[y+offset[1]][x+offset[0]],
                    'direction':d})
        return neighbours
