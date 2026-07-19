from dataclasses import dataclass, field
import heapq
from parse import Map, Hub


@dataclass
class Nodes:
    hub: Hub
    neighbors: list["Nodes"] = field(default_factory=list)


class Graph:
    def __init__(self, map: Map):
        self.nodes = {}
        self.map = map
        self.create_graph()

    def create_graph(self):

        for hub in self.map.hubs + [self.map.start, self.map.end]:
            self.nodes[hub.name] = Nodes(hub)

        for connection in self.map.connections:
            start = self.nodes[connection.start.name]
            end = self.nodes[connection.end.name]

            start.neighbors.append(end)
            end.neighbors.append(start)

    def find_path_bfs(self, start_name: str, end_name: str):
        queue = []
        visited = set()
        queue.append([self.nodes[start_name].hub])
        visited.add(self.nodes[start_name].hub.name)

        while queue:
            path = queue.pop(0)
            current = path[-1]
            if current.name == self.nodes[end_name].hub.name:
                return path
            for neigbotrs in self.nodes[current.name].neighbors:
                if neigbotrs.hub.name not in visited:
                    visited.add(neigbotrs.hub.name)
                    new_path = path.copy()
                    new_path.append(neigbotrs.hub)
                    queue.append(new_path)

        return False

    # def find_path_dijkstra():
