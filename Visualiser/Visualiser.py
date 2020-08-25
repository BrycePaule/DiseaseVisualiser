import pygame
import random

from Visualiser.Node import Node
from DiseaseAlgorithm.DiseaseSpread import DiseaseSpread

from Settings.VisualiserSettings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from Settings.VisualiserSettings import VIS_WINDOW_SIZE, VIS_NODE_WIDTH, NODE_SIZE, NODE_COUNT
from Settings.VisualiserSettings import ALGORITHM_CALL_STEP, TIMED_DAYS, ANIMATE_NODES
from Settings.VisualiserSettings import BG_COLOUR, GRID_BORDER_COLOUR
from Settings.AlgorithmSettings import DAY_LIMIT


class Visualiser:

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Disease Spread Visualiser')

    def __init__(self, ):
        self.clock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.grid_surf = pygame.Surface((VIS_WINDOW_SIZE, VIS_WINDOW_SIZE))

        self.grid = [[Node() for _ in range(VIS_NODE_WIDTH)] for _ in range(VIS_NODE_WIDTH)]
        self.grid_sorted = [[Node() for _ in range(VIS_NODE_WIDTH)] for _ in range(VIS_NODE_WIDTH)]
        self.sort_toggle = False
        self.nodes_updated_since_draw = False

        self.day_limit = DAY_LIMIT
        self.spread = DiseaseSpread()
        self.day = 0
        self.daily_stats = {}
        self.nodes = self.nodes = {
            'healthy': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'infected': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'recovered': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'dead': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},

            'total': {'nodes': [], 'excess': []},
        }

        self.time_step = ALGORITHM_CALL_STEP   # 1000 = 1s
        self.time_count = pygame.time.get_ticks()

        self.animate_nodes = ANIMATE_NODES
        self.disease_algorithm_runtime = 0


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_SPACE:
                    self.sort_toggle = not self.sort_toggle


    def run(self):
        for i in range(1):
            self.spread.population.people[i].infect()

        while self.day <= self.day_limit:

            self.clock.tick(FPS)
            self.events()

            if self.day_has_passed():
                if self.animate_nodes:
                    if self.day < TIMED_DAYS:
                        start = pygame.time.get_ticks()
                        self.daily_stats[self.day] = self.spread.pass_day(self.day)
                        runtime = pygame.time.get_ticks() - start
                        self.disease_algorithm_runtime = (self.disease_algorithm_runtime + runtime) // 2
                    else:
                        self.daily_stats[self.day] = self.spread.pass_day(self.day)
                else:
                    self.daily_stats[self.day] = self.spread.pass_day(self.day)

                # self.write_daily_stats_to_file()

                self.nodes_update()
                self.day += 1

            self.draw()

            # if self.day > 0:
            #     if self.spread.is_finished(self.day):
            #         return


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

        for y in range(VIS_NODE_WIDTH):
            for x in range(VIS_NODE_WIDTH):
                if not self.sort_toggle:
                    node_surf = self.grid[y][x].draw()
                    self.grid_surf.blit(node_surf, (x * NODE_SIZE, y * NODE_SIZE))

                else:
                    if self.nodes_updated_since_draw:
                        self.nodes_sort()
                    node_surf = self.grid_sorted[y][x].draw()
                    self.grid_surf.blit(node_surf, (x * NODE_SIZE, y * NODE_SIZE))

        self.nodes_updated_since_draw = False


    def day_has_passed(self):
        if pygame.time.get_ticks() > self.time_count + self.time_step:
            self.time_count = pygame.time.get_ticks()
            return True
        else:
            return False


    def nodes_update(self):
        self.nodes_tally()
        self.nodes_calc_visualiser_spread_diff()
        self.nodes_convert_excesses()
        self.nodes_updated_since_draw = True


    def nodes_tally(self):
        self.nodes = {
            'healthy': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'infected': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'recovered': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'dead': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},

            'total': {'nodes': [], 'excess': []},
        }

        for y in range(VIS_NODE_WIDTH):
            for x in range(VIS_NODE_WIDTH):
                node = self.grid[y][x]
                if node.status == 0:
                    self.nodes['healthy']['nodes'].append(node)
                    self.nodes['total']['nodes'].append(node)
                if node.status in [1, 2]:
                    self.nodes['infected']['nodes'].append(node)
                    self.nodes['total']['nodes'].append(node)
                if node.status == 3:
                    self.nodes['recovered']['nodes'].append(node)
                    self.nodes['total']['nodes'].append(node)
                if node.status == 4:
                    self.nodes['dead']['nodes'].append(node)
                    self.nodes['total']['nodes'].append(node)

        self.nodes['healthy']['percentage'] = round((len(self.nodes['healthy']['nodes']) / len(self.nodes['total']['nodes']) * 100), 2)
        self.nodes['infected']['percentage'] = round((len(self.nodes['infected']['nodes']) / len(self.nodes['total']['nodes']) * 100), 2)
        self.nodes['recovered']['percentage'] = round((len(self.nodes['recovered']['nodes']) / len(self.nodes['total']['nodes']) * 100), 2)
        self.nodes['dead']['percentage'] = round((len(self.nodes['dead']['nodes']) / len(self.nodes['total']['nodes']) * 100), 2)


    def nodes_calc_visualiser_spread_diff(self):
        node_types = [
            ('healthy', 'healthy_percentage'),
            ('infected', 'infected_percentage'),
            ('recovered', 'recovered_percentage'),
            ('dead', 'dead_percentage')
        ]

        for node, percent in node_types:

            spread_percent = self.daily_stats[self.day][percent]
            excess_node_count = round((self.nodes[node]['percentage'] - spread_percent) / 100 * NODE_COUNT)

            if excess_node_count > 0:
                if not self.sort_toggle:
                    self.nodes['total']['excess'] += random.sample(self.nodes[node]['nodes'], excess_node_count)
                else:
                    self.nodes['total']['excess'] += self.nodes[node]['nodes'][:excess_node_count]
            elif excess_node_count < 0:
                self.nodes[node]['needed'] = round((spread_percent - self.nodes[node]['percentage']) / 100 * NODE_COUNT)


    def nodes_convert_excesses(self):
        for node in self.nodes['total']['excess']:
            if self.nodes['dead']['needed'] > 0:
                node.convert_dead()
                self.nodes['dead']['needed'] -= 1
                continue

            if self.nodes['recovered']['needed'] > 0:
                node.convert_recovered()
                self.nodes['recovered']['needed'] -= 1
                continue

            if self.nodes['infected']['needed'] > 0:
                node.convert_infected()
                self.nodes['infected']['needed'] -= 1
                continue

            if self.nodes['healthy']['needed'] > 0:
                node.convert_healthy()
                self.nodes['healthy']['needed'] -= 1
                continue


    def nodes_sort(self):
        sorted_flat_nodes = sorted([node for line in self.grid for node in line], key=lambda node: node.status, reverse=True)

        bounds = [0, VIS_NODE_WIDTH]
        for i in range(VIS_NODE_WIDTH):
            self.grid_sorted[i] = sorted_flat_nodes[bounds[0]:bounds[1]]
            bounds = [bounds[0] + 10, bounds[1] + 10]


    def write_daily_stats_to_file(self):
        with open(f'./daily_stats.txt', mode='w') as f:
            for key, value in self.daily_stats.items():
                f.write(f'-----------------------------\n')
                f.write(f'Day: {key}\n')

                for k, v in value.items():
                    f.write(f'{k} - {v}\n')

                f.write('\n')