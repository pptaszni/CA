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
        self.directions = ['E','SE','SW','W','NW','NE']
        self.rotations = ['Left','Right']
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
    def Transferable(self,coords,offset):
        if (coords[0] + offset[0] >= 0 and
                coords[1] + offset[1] >= 0 and
                coords[0] + offset[0] < self.xBorder and
                coords[1] + offset[1] < self.yBorder):
            field = self._map[coords[1]+offset[1]][coords[0]+offset[0]]
            try:
                if not field.transferable:
                    return False
            except:
                return False
        else:
            try:
                if not self._map[coords[1]][coords[0]].border:
                    return False
            except:
                return False
        return True
    def GetNeighbours(self,coords,hold):
        y = int(coords[1])
        x = int(coords[0])
        phi = coords[2]
        yEven = not bool(y%2)
        neighbours = []
        for d in self.directions:
            offset = self.MapOffset(yEven,d)
            if (x+offset[0] >= 0 and y+offset[1] >= 0 and 
                    x+offset[0] < self.xBorder and
                    y+offset[1] < self.yBorder):
                coords = (x+offset[0],y+offset[1],phi)
                field = self._map[y+offset[1]][x+offset[0]]
                movable = False
                try:
                    movable = field.movable
                except:
                    movable = False
                if not movable:
                    continue
                if hold:
                    itemOffset = self.MapOffset(yEven,phi)
                    itemCoords = (x+itemOffset[0],y+itemOffset[1])
                    itemYEven = not bool(itemCoords[1]%2)
                    itemNewOffset = self.MapOffset(itemYEven,d)
                    if not self.Transferable(itemCoords,itemNewOffset):
                        continue
                neighbours.append({'coords':coords,
                    'field':field,
                    'direction':d})
        for r in self.rotations:
            d = None
            if r == 'Left':
                d = self.directions[(self.directions.index(phi)
                    -1)%len(self.directions)]
            elif r == 'Right':
                d = self.directions[(self.directions.index(phi)
                    -1)%len(self.directions)]
            if hold:
                field = self._map[y][x]
                offset1 = self.MapOffset(yEven,phi)
                offset2 = self.MapOffset(yEven,d)
                offset2 = (offset2[0]-offset1[0],offset2[1]-offset1[1])
                if not self.Transferable((x+offset1[0],y+offset1[1]),
                        offset2):
                    continue
            neighbours.append({'coords':(x,y,d),
                'field':field,
                'direction':r})
        return neighbours
