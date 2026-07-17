import pygame as pg
from parse import Map
from drone import Drone

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Visualizer:
    def __init__(self, map: Map, drones: list[Drone]):
        self.map = map
        self.zoom = 50
        self.offset_x = 100
        self.offset_y = 100
        self.drones = drones
        self.run = False

    def make_window(self):
        pg.init()
        WIDTH = 1500
        HEIGHT = 800
        font = pg.font.Font(None, 18)

        screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Fly-In (jtruckse)")

        running = True

        while running:
            keys = pg.key.get_pressed()
            for event in pg.event.get():
                if event.type == pg.MOUSEWHEEL:
                    if event.y > 0:
                        self.zoom *= 1.1
                    if event.y < 0:
                        self.zoom /= 1.1

                if event.type == pg.QUIT or keys[pg.K_ESCAPE]:
                    running = False

            screen.fill((200, 200, 255))
            for connection in self.map.connections:
                x_start = (connection.start.x * self.zoom +
                           0.1 * WIDTH + self.offset_x)
                y_start = (connection.start.y * self.zoom +
                           0.5 * HEIGHT + self.offset_y)
                x_end = (connection.end.x * self.zoom +
                         0.1 * WIDTH + self.offset_x)
                y_end = (connection.end.y * self.zoom +
                         0.5 * HEIGHT + self.offset_y)
                pg.draw.line(screen, BLACK, (x_start, y_start),
                                            (x_end, y_end))
            for hub in self.map.hubs + [self.map.start, self.map.end]:
                x = hub.x * self.zoom + 0.1 * WIDTH + self.offset_x
                y = hub.y * self.zoom + 0.5 * HEIGHT + self.offset_y
                pg.draw.circle(screen, WHITE, (x, y), self.zoom / 5)
                pg.draw.circle(screen, hub.color, (x, y), self.zoom / 5.15)
                text = font.render(hub.name, True, BLACK)
                screen.blit(text, (x - 6, y + 12))

            if keys[pg.K_a]:
                self.offset_x += self.zoom / self.zoom * 0.3
            if keys[pg.K_s]:
                self.offset_y -= self.zoom / self.zoom * 0.3
            if keys[pg.K_d]:
                self.offset_x -= self.zoom / self.zoom * 0.3
            if keys[pg.K_w]:
                self.offset_y += self.zoom / self.zoom * 0.3

            if keys[pg.K_SPACE]:
                self.run = True
            for drone in self.drones:
                if drone.current < len(drone.path):
                    target = drone.path[drone.current]
                    speed = 0.005
                    dx = target.x - drone.x
                    dy = target.y - drone.y
                    if self.run is True:
                        drone.x += dx * speed
                        drone.y += dy * speed

            for drone in self.drones:
                d_x = drone.x * self.zoom + 0.1 * WIDTH + self.offset_x
                d_y = drone.y * self.zoom + 0.5 * HEIGHT + self.offset_y
                pg.draw.circle(screen, drone.color, (d_x, d_y), self.zoom / 6)

                distance = ((target.x - drone.x)**2 +
                            (target.y - drone.y)**2)**0.5

                if distance < 0.05:
                    drone.x = target.x
                    drone.y = target.y
                    drone.current += 1

            pg.display.flip()
        pg.quit()
