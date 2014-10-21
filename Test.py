import unittest
from AStar import AStar
from Map import Map
from Unit import CreateUnitInstances
from Field import Field
import pickle
import random

mock_server_resp = '<?xml version="1.0"?> <game><general><timeSec>0.19850182533264</timeSec><roundNum>4</roundNum><amountOfPoints>0</amountOfPoints></general><units><unit id="3317" x="1" y="2" hp="97" status="" action="" orientation="NE" level="0" player="1"><sees direction="NE"><background>green</background></sees><sees direction="E"><background>green</background></sees><sees direction="SE"><background>green</background></sees><sees direction="SW"><background>green</background></sees><sees direction="W"><building player="1">base</building><background>green</background></sees><sees direction="NW"><background>green</background></sees></unit></units></game>'

class AStarTests(unittest.TestCase):

    def setUp(self):
        fileObj = open('map.dat','r')
        self._map = pickle.load(fileObj)
        fileObj.close()
        self.aStarInstance = AStar(self._map, (1,0),(5,4))

    def test_astar_starts_good(self):
        a = self.aStarInstance
        self.assertEqual(a.Start(),{'status':'OK','direction': 'SE', 'cost': 6})

    def test_heurisic_cost_calculated(self):
        a = self.aStarInstance
        x = (1,1)
        y = (4,5)
        self.assertEqual(a.HeuristicCost(x,y),25)

    def test_passage_cost_on_different_field_types(self):
        a = self.aStarInstance
        xBorder = self._map.xBorder
        yBorder = self._map.yBorder
        xRange = range(0,xBorder)
        yRange = range(0,yBorder)
        for y in yRange:
            for x in xRange:
                neighbours = self._map.GetNeighbours((x,y))
                for nei in neighbours:
                    self.assertIn(a.PassageCost(nei['field']),
                            [a.normalCost,a.redCost,a.unknownCost,a.infinity])

if __name__ == '__main__':
    unittest.main()
