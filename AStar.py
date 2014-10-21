import logging

class AStar():

    def __init__(self, m, start, goal):
        self._map = m
        self.start = start
        self.goal = goal
        self.infinity = 10**10
        self.normalCost = 1
        self.redCost = 2
        self.unknownCost = 3
        self.errorCost = -1

    def Start(self):
        closed_set = [] # touples of coordinates (x,y)
        open_set = [] # dicts: {coords, f_score}
        came_from = {}
        g_score = {}
        f_score = {}
        start = self.start
        goal = self.goal
        distance = self.HeuristicCost(start, goal) 
        open_set.append({
            'coords': start,
            'f_score': distance
            })
        g_score[str(start[0])+','+str(start[1])] = 0
        f_score[str(start[0])+','+str(start[1])] = distance
        while len(open_set) != 0:
            current = open_set.pop()
            current_key = (str(current['coords'][0])+','+
                    str(current['coords'][1]))
            if current['coords'] == goal:
                return self.ReconstructPath(came_from)

            closed_set.append(current['coords'])
            neighbours = self._map.GetNeighbours(current['coords'])
            for nei in neighbours:
                if nei['coords'] in closed_set:
                    continue
                tentative_g_score = (g_score[current_key] + 
                        self.PassageCost(nei['field']))
                nei_key = (str(nei['coords'][0])+','+
                        str(nei['coords'][1]))
                exists_in_openset = False
                for item in open_set:
                    if item['coords'] == nei['coords']:
                        exists_in_openset = True
                        break
                if not exists_in_openset or (exists_in_openset and 
                        tentative_g_score < g_score[nei_key]):
                    came_from[nei_key] = {'coords': current['coords'],
                            'direction': nei['direction']}
                    g_score[nei_key] = tentative_g_score
                    f_score[nei_key] = (g_score[nei_key] + 
                            self.HeuristicCost(nei['coords'],goal))
                    if not exists_in_openset:
                        open_set.append({
                            'coords': nei['coords'],
                            'f_score': f_score[nei_key]
                            })
                        open_set.sort(key=lambda x: x['f_score'],reverse=True)
        return {'status': 'NOK'}

    def HeuristicCost(self, start, goal):
        return (goal[0]-start[0])**2 + (goal[1]-start[1])**2
    def PassageCost(self, field):
        if field == None:
            return self.unknownCost
        if not field.movable:
            return self.infinity
        if field.background['type'] == 'red':
            return self.redCost
        elif (field.background['type'] == 'green' or 
                field.background['type'] == 'orange'):
            return self.normalCost
        return self.errorCost
    def ReconstructPath(self, came_from):
        goal_key = str(self.goal[0])+','+str(self.goal[1])
        current = self.goal
        total_cost = 0
        direction = 'Unknown'
        map_direction = {
                'E': 'W',
                'SE': 'NW',
                'SW': 'NE',
                'W': 'E',
                'NW': 'SE',
                'NE': 'SW'
                }
        logging.debug(str(came_from))
        while current != self.start:
            current_key = str(current[0])+','+str(current[1])
            total_cost = total_cost + self.PassageCost(
                    self._map._map[current[1]][current[0]])
            direction = came_from[current_key]['direction']
            current = came_from[current_key]['coords']
        return {'status': 'OK', 'direction': direction, 'cost': total_cost}
