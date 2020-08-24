import pygame
import random

from Visualiser.Node import Node
from DiseaseAlgorithm.DiseaseSpread import DiseaseSpread
from Settings.VisualiserSettings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, VISUALISER_WINDOW_SIZE, VISUALISER_NODE_WIDTH, NODE_SIZE, NODE_COUNT, BG_COLOUR, GRID_BORDER_COLOUR
from Settings.AlgorithmSettings import DAY_LIMIT


class Visualiser:

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Disease Spread Visualiser')

    def __init__(self, ):
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.grid_surf = pygame.Surface((VISUALISER_WINDOW_SIZE, VISUALISER_WINDOW_SIZE))

        self.grid = [[Node() for _ in range(VISUALISER_NODE_WIDTH)] for _ in range(VISUALISER_NODE_WIDTH)]

        self.day_limit = DAY_LIMIT
        self.spread = DiseaseSpread()
        self.day = 0
        self.daily_stats = {}

        self.time_step = 500   # 1000 = 1s
        self.time_count = pygame.time.get_ticks()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()


    def draw(self):
        self.screen.fill(BG_COLOUR)

        self.draw_grid()

        self.screen.blit(
            self.grid_surf,
            ((SCREEN_WIDTH // 2) - (self.grid_surf.get_width() // 2),
             (SCREEN_HEIGHT // 2) - (self.grid_surf.get_height() // 2))
        )

        pygame.display.update()


    def draw_grid(self):
        self.grid_surf.fill((0, 0, 0))

        for y in range(VISUALISER_NODE_WIDTH):
            for x in range(VISUALISER_NODE_WIDTH):
                node_surf = self.grid[y][x].draw()
                self.grid_surf.blit(node_surf, (x * NODE_SIZE, y * NODE_SIZE))


    def run(self):
        for i in range(1):
            self.spread.population.people[i].infect()

        while self.day <= self.day_limit:

            self.clock.tick(FPS)
            self.events()


            if pygame.time.get_ticks() > self.time_count + self.time_step:
                self.time_count = pygame.time.get_ticks()
                self.daily_stats[self.day] = self.spread.pass_day(self.day)

                if self.day > 0:
                    self.update_nodes()

                self.day += 1

            self.draw()

            # if self.day > 0:
            #     if self.spread.is_finished(self.day):
            #         return


    def update_nodes(self):
        #
        # for line in self.grid:
        #     random.shuffle(line)
        # random.shuffle(self.grid)

        healthy, infected, recovered, dead = [], [], [], []

        for y in range(VISUALISER_NODE_WIDTH):
            for x in range(VISUALISER_NODE_WIDTH):
                node = self.grid[y][x]
                if node.status == 0:
                    healthy.append(node)
                if node.status in [1, 2]:
                    infected.append(node)
                if node.status == 3:
                    recovered.append(node)
                if node.status == 4:
                    dead.append(node)

        excess_nodes = []
        healthy_diff, infected_diff, recovered_diff, dead_diff = 0, 0, 0, 0

        curr_percent = round(len(healthy) / NODE_COUNT * 100, 2)
        if (spread_percent := self.daily_stats[self.day]['healthy_percentage']) < curr_percent:
            excess_nodes += random.sample(healthy, round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        else:
            healthy_diff = (spread_percent - curr_percent) / 100 * NODE_COUNT

        curr_percent = round(len(infected) / NODE_COUNT * 100, 2)
        if (spread_percent := self.daily_stats[self.day]['infected_percentage']) < curr_percent:
            excess_nodes += random.sample(infected, round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        else:
            infected_diff = (spread_percent - curr_percent) / 100 * NODE_COUNT

        curr_percent = round(len(recovered) / NODE_COUNT * 100, 2)
        if (spread_percent := self.daily_stats[self.day]['recovered_percentage']) < curr_percent:
            excess_nodes += random.sample(recovered, round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        else:
            recovered_diff = (spread_percent - curr_percent) / 100 * NODE_COUNT

        curr_percent = round(len(dead) / NODE_COUNT * 100, 2)
        if (spread_percent := self.daily_stats[self.day]['dead_percentage']) < curr_percent:
            excess_nodes += random.sample(dead, round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        else:
            dead_diff = (spread_percent - curr_percent) / 100 * NODE_COUNT

        for node in excess_nodes:
            for i in range(round(healthy_diff)):
                node.status = 0
            for i in range(round(infected_diff)):
                node.status = 1
            for i in range(round(recovered_diff)):
                node.status = 3
            for i in range(round(dead_diff)):
                node.status = 4

        # print(f'healthy_diff: {healthy_diff}')
        # print(f'infected_diff: {infected_diff}')
        # print(f'recovered_diff: {recovered_diff}')
        # print(f'dead_diff: {dead_diff}')
        # print(f'Excess: {len(excess_nodes)}')