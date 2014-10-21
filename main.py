# Main Application for CodeArena tournament

from ConnectionsAndParsing import ConnectToServer
from CommandInterpreter import InterpretFirstResponse
from InferenceEngine import InferenceEngine
from Unit import CreateUnitInstances
from Map import Map
import logging

def StartGame():
    s, resp = ConnectToServer()
    game_id = InterpretFirstResponse(resp)
    if game_id < 0:
        print 'Exiting program ... '
        s.close()
    logging.basicConfig(filename='game_'+game_id+'.log',
            level=logging.DEBUG, 
            format='%(asctime)s %(levelname)s:%(message)s')
    logging.info('Game '+game_id+' started!')

    units = CreateUnitInstances(resp)
    unit = units[0]
    m = Map(unit.x, unit.y, unit.surroundings)
    infer = InferenceEngine(units, m, s)
    infer.Start()
    s.close()

StartGame()
