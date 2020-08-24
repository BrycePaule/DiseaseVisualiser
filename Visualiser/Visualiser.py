import pygame
import random
import time

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
        self.grid_sorted = [[Node() for _ in range(VISUALISER_NODE_WIDTH)] for _ in range(VISUALISER_NODE_WIDTH)]
        self.sort_toggle = False

        self.day_limit = DAY_LIMIT
        self.spread = DiseaseSpread()
        self.day = 0
        self.daily_stats = {}
        self.nodes = {
            'healthy': ([], 0),
            'infected': ([], 0),
            'recovered': ([], 0),
            'dead': ([], 0)
        }

        self.time_step = 500   # 1000 = 1s
        self.time_count = pygame.time.get_ticks()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    self.sort_nodes()


    def draw(self):
        self.screen.fill(BG_COLOUR)

        font = pygame.font.SysFont('Arial', 30)
        text = font.render(f'Day: {self.day}', 1, (255, 255, 255))
        self.screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))

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
                if not self.sort_toggle:
                    node_surf = self.grid[y][x].draw()
                    self.grid_surf.blit(node_surf, (x * NODE_SIZE, y * NODE_SIZE))
                else:
                    node_surf = self.grid_sorted[y][x].draw()
                    self.grid_surf.blit(node_surf, (x * NODE_SIZE, y * NODE_SIZE))


    def run(self):
        for i in range(1):
            self.spread.population.people[i].infect()

        while self.day <= self.day_limit:

            self.clock.tick(FPS)
            self.events()

            if self.time_to_pass_day():
                self.daily_stats[self.day] = self.spread.pass_day(self.day)

                # with open(f'./daily_stats.txt', mode='w') as f:
                #     for key, value in self.daily_stats.items():
                #         f.write(f'-----------------------------\n')
                #         f.write(f'Day: {key}\n')
                #
                #         for k, v in value.items():
                #             f.write(f'{k} - {v}\n')
                #
                #         f.write('\n')

                if self.day > 0:
                    self.calc_node_counts()
                    self.update_nodes()

                self.day += 1

            self.draw()

            # if self.day > 0:
            #     if self.spread.is_finished(self.day):
            #         return


    def time_to_pass_day(self):
        if pygame.time.get_ticks() > self.time_count + self.time_step:
            self.time_count = pygame.time.get_ticks()
            return True
        else:
            return False


    def calc_node_counts(self):
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

        self.nodes['healthy'] = (healthy, len(healthy))
        self.nodes['infected'] = (infected, len(infected))
        self.nodes['recovered'] = (recovered, len(recovered))
        self.nodes['dead'] = (dead, len(dead))


    def update_nodes(self):
        excess_nodes = []
        healthy_needed, infected_needed, recovered_needed, dead_needed = 0, 0, 0, 0

        curr_percent = round(self.nodes['healthy'][1] / NODE_COUNT * 100, 2)
        spread_percent = self.daily_stats[self.day]['healthy_percentage']
        if spread_percent < curr_percent:
            excess_nodes += random.sample(self.nodes['healthy'][0], round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        elif spread_percent > curr_percent:
            healthy_needed = (spread_percent - curr_percent) / 100 * NODE_COUNT

        curr_percent = round(self.nodes['infected'][1] / NODE_COUNT * 100, 2)
        spread_percent = self.daily_stats[self.day]['infected_percentage']
        if spread_percent < curr_percent:
            excess_nodes += random.sample(self.nodes['infected'][0], round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        elif spread_percent > curr_percent:
            infected_needed = (spread_percent - curr_percent) / 100 * NODE_COUNT

        curr_percent = round(self.nodes['recovered'][1] / NODE_COUNT * 100, 2)
        spread_percent = self.daily_stats[self.day]['recovered_percentage']
        if spread_percent < curr_percent:
            excess_nodes += random.sample(self.nodes['recovered'][0], round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        elif spread_percent > curr_percent:
            recovered_needed = (spread_percent - curr_percent) / 100 * NODE_COUNT

        curr_percent = round(self.nodes['dead'][1] / NODE_COUNT * 100, 2)
        spread_percent = self.daily_stats[self.day]['dead_percentage']
        if spread_percent < curr_percent:
            excess_nodes += random.sample(self.nodes['dead'][0], round((curr_percent - spread_percent) / 100 * NODE_COUNT))
        elif spread_percent > curr_percent:
            dead_needed = (spread_percent - curr_percent) / 100 * NODE_COUNT


        for node in excess_nodes:
            if healthy_needed:
                node.convert_healthy()
                healthy_needed -= 1
                continue

            if infected_needed:
                node.convert_infected()
                infected_needed -= 1
                continue

            if recovered_needed:
                node.convert_recovered()
                recovered_needed -= 1
                continue

            if dead_needed:
                node.convert_dead()
                dead_needed -= 1
                continue


    def sort_nodes(self):
        self.sort_toggle = not self.sort_toggle
        sorted_flat_nodes = sorted([node for line in self.grid for node in line], key=lambda node: node.status, reverse=True)

        bounds = [0, VISUALISER_NODE_WIDTH]
        for i in range(VISUALISER_NODE_WIDTH):
            self.grid_sorted[i] = sorted_flat_nodes[bounds[0]:bounds[1]]
            bounds = [bounds[0] + 10, bounds[1] + 10]