import pygame as pg
from parse import Map, COLORS
from drone import Drone
from simulation import Move

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Visualizer:
    def __init__(self, moves: list[Move], map: Map, drones: list[Drone]):
        self.map = map
        self.zoom = 50
        self.offset_x = 100
        self.offset_y = 100
        self.drones = drones
        self.run = False
        self.moves = moves
        self.turn = 0

    def make_window(self):
        pg.init()
        WIDTH = 1500
        HEIGHT = 800
        font = pg.font.Font(None, 18)
        progress = 0.0
        pause = False
        pause_start = 0
        speed = 0.005

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
                pg.draw.circle(screen, COLORS[hub.color],
                               (x, y), self.zoom / 5.15)
                text = font.render(hub.name, True, BLACK)
                screen.blit(text, (x - 6, y + 12))

            if keys[pg.K_a]:
                self.offset_x += self.zoom / self.zoom * 0.55
            if keys[pg.K_s]:
                self.offset_y -= self.zoom / self.zoom * 0.55
            if keys[pg.K_d]:
                self.offset_x -= self.zoom / self.zoom * 0.55
            if keys[pg.K_w]:
                self.offset_y += self.zoom / self.zoom * 0.55
            if keys[pg.K_SPACE]:
                self.run = True

            if self.turn < 1 and self.run is False:
                for d in self.drones:
                    x = d.position.x * self.zoom + 0.1 * WIDTH + self.offset_x
                    y = d.position.y * self.zoom + 0.5 * HEIGHT + self.offset_y
                    pg.draw.circle(screen, d.color, (x, y), self.zoom / 6)
                    t_id = font.render(f"D{d.id}", True, BLACK)
                    screen.blit(t_id, (x, y))

            elif self.turn < len(self.moves):
                current_turn = self.moves[self.turn]
                for m in current_turn:
                    d_id = m.drone.id
                    start = m.start
                    target = m.end
                    dx = target.x - start.x
                    dy = target.y - start.y
                    x = start.x + dx * progress
                    y = start.y + dy * progress
                    d_x = x * self.zoom + 0.1 * WIDTH + self.offset_x
                    d_y = y * self.zoom + 0.5 * HEIGHT + self.offset_y
                    pg.draw.circle(screen, m.drone.color, (d_x, d_y), self.zoom / 6)
                    t_id = font.render(f"D{d_id}", True, BLACK)
                    screen.blit(t_id, (d_x, d_y))

                if not pause and self.run is True:
                    progress += speed

                if progress >= 1.0 and pause is False:
                    pause = True
                    pause_start = pg.time.get_ticks()

                if pause is True:
                    if pg.time.get_ticks() - pause_start > 500:
                        pause = False
                        progress = 0.0
                        self.turn += 1

            pg.display.flip()
        pg.quit()
