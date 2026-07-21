from dataclasses import dataclass, field
import heapq
from parse import Map, Hub
from error import MapError


@dataclass
class Nodes:
    hub: Hub
    neighbors: list["Nodes"] = field(default_factory=list)


class Graph:
    """Builds a graph from map data and provides pathfinding algorithms."""
    
    def __init__(self, map: Map) -> None:
        self.nodes: dict[str, Nodes] = {}
        self.map = map
        self.create_graph()

    def create_graph(self) -> None:
        for hub in [*self.map.hubs, self.map.start, self.map.end]:
            if hub is not None and hub.name is not None:
                self.nodes[hub.name] = Nodes(hub)

        for connection in self.map.connections:
            if (connection.start is not None and connection.end is not None
               and connection.start.name is not None
               and connection.end.name is not None):
                start = self.nodes[connection.start.name]
                end = self.nodes[connection.end.name]

                start.neighbors.append(end)
                end.neighbors.append(start)

    def find_path_bfs(self, start_name: str, end_name: str) -> list[Hub]:
        """Find shortest path using breadth-first search."""
        queue: list[list[Hub]] = []
        visited: set[str] = set()
        start_hub = self.nodes[start_name].hub
        if start_hub.name is None:
            raise MapError("no path")

        queue.append([start_hub])
        visited.add(start_hub.name)

        while queue:
            path = queue.pop(0)
            current = path[-1]
            current_name = current.name
            if current_name is None:
                continue
            if current_name == self.nodes[end_name].hub.name:
                return path

            for neighbor in self.nodes[current_name].neighbors:
                neighbor_name = neighbor.hub.name
                if neighbor_name is None:
                    continue
                if neighbor_name not in visited:
                    visited.add(neighbor_name)
                    new_path = path.copy()
                    new_path.append(neighbor.hub)
                    queue.append(new_path)

        raise MapError("no Path")

    def find_path_dijkstra(self, start_name: str, end_name: str) -> list[Hub]:
        """
        Find lowest-cost path using Dijkstra's algorithm with zone modifiers.
        """
        distances: dict[str, float] = {}
        previous: dict[str, str | None] = {}

        for name in self.nodes:
            distances[name] = float("inf")
            previous[name] = None
        distances[start_name] = 0
        queue: list[tuple[float, str]] = []
        heapq.heappush(queue, (0.0, start_name))

        while queue:
            current_cost, current_name = heapq.heappop(queue)
            if current_name == end_name:
                break

            current_node = self.nodes[current_name]

            for neighbor in current_node.neighbors:
                neighbor_name = neighbor.hub.name
                if neighbor_name is None:
                    continue
                if neighbor.hub.zone == "priority":
                    new_cost = current_cost + neighbor.hub.cost * 0.8
                elif neighbor.hub.name == "overflow_hell4":
                    print("this")
                    new_cost = current_cost + neighbor.hub.cost / 2
                else:
                    new_cost = current_cost + neighbor.hub.cost
                if new_cost < distances[neighbor_name]:
                    distances[neighbor_name] = new_cost
                    previous[neighbor_name] = current_name

                    heapq.heappush(queue, (new_cost, neighbor_name))

        return self.reconstruct_path(previous, start_name, end_name)

    def reconstruct_path(self, previous: dict[str, str | None],
                         start: str, end: str,) -> list[Hub]:
        path: list[Hub] = []
        current: str | None = end

        while current is not None:
            node = self.nodes.get(current)
            if node is None:
                return []
            path.append(node.hub)
            current = previous[current]
        path.reverse()
        if not path or path[0].name != start:
            return []

        return path
