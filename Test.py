import unittest
from AStar import AStar
from Map import Map
from Unit import CreateUnitInstances
from Field import Field
import pickle
import random
from mock import Mock

mock_server_resp = '<?xml version="1.0"?> <game><general><timeSec>0.19850182533264</timeSec><roundNum>4</roundNum><amountOfPoints>0</amountOfPoints></general><units><unit id="3317" x="1" y="2" hp="97" status="" action="" orientation="NE" level="0" player="1"><sees direction="NE"><background>green</background></sees><sees direction="E"><background>green</background></sees><sees direction="SE"><background>green</background></sees><sees direction="SW"><background>green</background></sees><sees direction="W"><building player="1">base</building><background>green</background></sees><sees direction="NW"><background>green</background></sees></unit></units></game>'

class AStarTests(unittest.TestCase):

    def setUp(self):
        fileObj = open('map.dat','r')
        self._map = pickle.load(fileObj)
        fileObj.close()
        self.aStarInstance = AStar(self._map, (1,0,'E'),(5,4,'E'))

    def test_dict_key_returns_good_key(self):
        dkey = self.aStarInstance.DictKey((1,2,'E'))
        self.assertEqual(dkey,'1,2,E')

    def test_astar_starts_good_in_basic_mode(self):
        a = self.aStarInstance
        self.assertEqual(a.Start(),{'status':'OK','direction': 'SE', 'cost': 6})

    def test_heurisic_cost_calculated(self):
        a = self.aStarInstance
        x = (1,1,'E')
        y = (4,5,'E')
        self.assertEqual(a.HeuristicCost(x,y),25)

    def test_passage_cost_on_different_field_types(self):
        a = self.aStarInstance
        xBorder = self._map.xBorder
        yBorder = self._map.yBorder
        xRange = range(0,xBorder)
        yRange = range(0,yBorder)
        for y in yRange:
            for x in xRange:
                try:
                    if not self._map[y][x].movable:
                        continue
                except:
                    continue
                neighbours = self._map.GetNeighbours((x,y,'E'),False)
                for nei in neighbours:
                    self.assertIn(a.PassageCost(nei['field']),
                            [a.normalCost,a.redCost,a.unknownCost])

class MapTests(unittest.TestCase):
    def setUp(self):
        fileObj = open('map.dat','r')
        self._map = pickle.load(fileObj)
        fileObj.close()
    def test_transferable(self):
        self.assertTrue(self._map.Transferable((1,1),(1,1)))
        self.assertTrue(not self._map.Transferable((5,3),(0,1)))
    def test_getneighbours_returns_neighbours_list(self):
        x = 1
        y = 2
        phi = 'E'
        neighbours = self._map.GetNeighbours((x,y,phi),hold=False)
        self.assertEqual(len(neighbours),7)
        for n in neighbours:
            self.assertEqual(len(n['coords']),3)
            self.assertTrue(isinstance(n['field'],
                self._map._map[y][x].__class__))
            self.assertTrue(n['direction'] in
                    ['E','SE','SW','W','NW','NE','Right','Left'])
        x = 1
        y = 2
        phi = 'SW'
        neighbours = self._map.GetNeighbours((x,y,phi),hold=True)
        self.assertEqual(len(neighbours),6)




if __name__ == '__main__':
    unittest.main()
