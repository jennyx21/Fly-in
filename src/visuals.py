import pygame as pg
from parse import Map, COLORS, Hub
from drone import Drone
from simulation import Move

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Visualizer:
    def __init__(
        self,
        moves: list[list[Move]],
        map: Map,
        drones: list[Drone],
    ) -> None:
        self.map = map
        self.zoom: float = 50.0
        self.offset_x: float = 100.0
        self.offset_y: float = 100.0
        self.drones = drones
        self.run = False
        self.moves = moves
        self.turn = 0

    def make_window(self) -> None:
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
                if connection.start is None or connection.end is None:
                    continue
                start_x = connection.start.x
                start_y = connection.start.y
                end_x = connection.end.x
                end_y = connection.end.y
                if start_x is None or start_y is None:
                    continue
                if end_x is None or end_y is None:
                    continue
                x_start = (start_x * self.zoom +
                           0.1 * WIDTH + self.offset_x)
                y_start = (start_y * self.zoom +
                           0.5 * HEIGHT + self.offset_y)
                x_end = (end_x * self.zoom +
                         0.1 * WIDTH + self.offset_x)
                y_end = (end_y * self.zoom +
                         0.5 * HEIGHT + self.offset_y)
                pg.draw.line(screen, BLACK, (x_start, y_start),
                                            (x_end, y_end))
            hub_list: list[Hub] = [
                hub for hub in [*self.map.hubs, self.map.start, self.map.end]
                if hub is not None
            ]
            for hub in hub_list:
                if hub.x is None or hub.y is None:
                    continue
                x = hub.x * self.zoom + 0.1 * WIDTH + self.offset_x
                y = hub.y * self.zoom + 0.5 * HEIGHT + self.offset_y
                pg.draw.circle(screen, WHITE, (x, y), self.zoom / 5)
                pg.draw.circle(screen, COLORS[hub.color],
                               (x, y), self.zoom / 5.15)
                text = font.render(hub.name or "", True, BLACK)
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
                    if d.position is None:
                        continue
                    if d.position.x is None or d.position.y is None:
                        continue
                    x = d.position.x * self.zoom + 0.1 * WIDTH + self.offset_x
                    y = d.position.y * self.zoom + 0.5 * HEIGHT + self.offset_y
                    pg.draw.circle(screen, d.color, (x, y), self.zoom / 6)
                    t_id = font.render(f"D{d.id}", True, BLACK)
                    screen.blit(t_id, (x, y))

            elif self.turn < len(self.moves):
                current_turn = self.moves[self.turn]
                for m in current_turn:
                    if m.start.x is None or m.start.y is None:
                        continue
                    if m.end.x is None or m.end.y is None:
                        continue
                    if m.start != m.end:
                        d_id = m.drone.id
                        start = m.start
                        target = m.end
                        start_x = start.x
                        start_y = start.y
                        target_x = target.x
                        target_y = target.y
                        if start_x is None or start_y is None:
                            continue
                        if target_x is None or target_y is None:
                            continue
                        dx = target_x - start_x
                        dy = target_y - start_y
                        x = start_x + dx * progress
                        y = start_y + dy * progress
                        d_x = x * self.zoom + 0.1 * WIDTH + self.offset_x
                        d_y = y * self.zoom + 0.5 * HEIGHT + self.offset_y
                        pg.draw.circle(screen, m.drone.color,
                                       (d_x, d_y), self.zoom / 6)
                        t_id = font.render(f"D{d_id}", True, BLACK)
                        screen.blit(t_id, (d_x, d_y))
                    else:
                        d_id = m.drone.id
                        xd = (m.start.x * self.zoom + 0.1
                              * WIDTH + self.offset_x)
                        yd = (m.start.y * self.zoom + 0.5 *
                              HEIGHT + self.offset_y)
                        pg.draw.circle(screen, m.drone.color,
                                       (xd, yd), self.zoom / 6)
                        t_id = font.render(f"D{d_id}", True, BLACK)
                        screen.blit(t_id, (xd, yd))

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
