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

    def find_path_dijkstra(self, start_name, end_name):
        distances = {}
        previous = {}

        for name in self.nodes:
            distances[name] = float("inf")
            previous[name] = None

        distances[start_name] = 0

        queue = []
        heapq.heappush(queue, (0, start_name))

        while queue:

            current_cost, current_name = heapq.heappop(queue)

            if current_name == end_name:
                break

            current_node = self.nodes[current_name]

            for neighbor in current_node.neighbors:

                neighbor_name = neighbor.hub.name
                if neighbor.hub.zone == "priority":
                    new_cost = (
                        current_cost +
                        neighbor.hub.cost * 0.8
                    )
                elif neighbor.hub.name == "overflow_hell4":
                    print("this")
                    new_cost = (
                        current_cost +
                        neighbor.hub.cost / 2
                    )
                else:
                    new_cost = (
                        current_cost +
                        neighbor.hub.cost
                    )

                if new_cost < distances[neighbor_name]:

                    distances[neighbor_name] = new_cost
                    previous[neighbor_name] = current_name

                    heapq.heappush(
                        queue,
                        (new_cost, neighbor_name)
                    )

        return self.reconstruct_path(
            previous,
            start_name,
            end_name
        )
    
    def reconstruct_path(self, previous, start, end):

        path = []
        current = end

        while current is not None:
            path.append(self.nodes[current].hub)
            current = previous[current]
        path.reverse()

        if path[0].name != start:
            return []

        return path