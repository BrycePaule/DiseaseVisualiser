import pygame
import random
import numpy as np
import cProfile

from Visualiser.Node import Node
from DiseaseAlgorithm.VirusSpreadProjection import VirusSpreadProjection
from DiseaseAlgorithm.VirusManager import VirusManager

from Settings.VisualiserSettings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from Settings.VisualiserSettings import VIS_WINDOW_SIZE, VIS_NODE_WIDTH
from Settings.VisualiserSettings import MIN_ALGORITHM_CALL_STEP, TIMED_DAYS, ANIMATE_NODES
from Settings.VisualiserSettings import BG_COLOUR, SCALE_ANIM_WITH_TIME
from Settings.AlgorithmSettings import DAY_LIMIT, STARTING_INFECTIONS

from GUI.UIElements.Button import Button
from GUI.UIElements.TextBox import TextBox
from GUI.UIElements.Text import Text
from GUI.UIElements.UIGroup import UIGroup


class Visualiser:

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Virus Spread Visualiser')

    def __init__(self):
        # RUNNING
        self.paused = True

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.grid_surf = pygame.Surface((VIS_WINDOW_SIZE, VIS_WINDOW_SIZE))
        self.UI_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        self.day_font = pygame.font.SysFont('Arial', 30)
        self.day_text = None

        # GRID SETTINGS
        self.grid_size = VIS_NODE_WIDTH
        self.node_count = self.grid_size * self.grid_size
        self.node_size = VIS_WINDOW_SIZE // self.grid_size

        self.grid = np.array([Node() for _ in range(self.grid_size ** 2)])
        self.grid_sorted = np.array([Node() for _ in range(self.grid_size ** 2)])
        self.sort_toggle = False
        self.nodes_updated_since_draw = True

        # VIRUS SETTINGS
        self.virus_manager = VirusManager()
        self.virus_spread_projection = VirusSpreadProjection(self.virus_manager.diseases['COVID-19'])
        self.day_limit = DAY_LIMIT
        self.day = 0
        self.daily_stats = {}
        self.nodes = {
            'healthy': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'infected': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'recovered': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'dead': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},

            'total': {'nodes': [], 'excess': []},
        }

        self.time_step = MIN_ALGORITHM_CALL_STEP   # 1000 = 1s
        self.time_count = pygame.time.get_ticks()

        self.animate_nodes = ANIMATE_NODES
        self.disease_algorithm_runtime = 0

        self.UIGroups = [UIGroup('Diseases', single_selection=True)]
        self.ui_elements = [
            Button('Start', 20, 90, 100, 30, ui_group=self.UIGroups[0], border=True, callback=self.callback_pause, toggleable=True, alt_text='Pause'),
            Button('Reset', 140, 90, 100, 30, ui_group=self.UIGroups[0], border=True, callback=self.callback_reset),

            Text(f'Virus Settings', 65, 160, 130, 30, align='centre'),
            Text(f'Diagnosis Time', 20, 200, 115, 30, font_size=14, align='left'),
            TextBox(f'{self.virus_manager.active_virus.diagnose_days}', 180, 200, 80, 30, font_size=12, text_suffix='(days)', border=True, callback=self.callback_diagnose_days, selectable=True, num_only=True),
            Text(f'Recovery Time', 20, 250, 110, 30, font_size=14, align='left'),
            TextBox(f'{self.virus_manager.active_virus.recovery_days}', 180, 250, 80, 30, font_size=12, text_suffix='(days)', border=True, callback=self.callback_recovery_days, selectable=True, num_only=True),
            Text(f'Infection Chance', 20, 300, 120, 30, font_size=14, align='left'),
            TextBox(f'{self.virus_manager.active_virus.infection_chance}', 180, 300, 80, 30, font_size=12, text_suffix='(%)', border=True, callback=self.callback_infection_chance, selectable=True, num_only=True),
            Text(f'Re-Infection Chance', 20, 350, 150, 30, font_size=14, align='left'),
            TextBox(f'{self.virus_manager.active_virus.reinfection_chance}', 180, 350, 80, 30, font_size=12, text_suffix='(%)', border=True, callback=self.callback_reinfection_chance, selectable=True, num_only=True),
            Text(f'Fatality Rate', 20, 400, 100, 30, font_size=14, align='left'),
            TextBox(f'{self.virus_manager.active_virus.fatality_chance}', 180, 400, 80, 30, font_size=12, text_suffix='(%)', border=True, callback=self.callback_fatality_chance, selectable=True, num_only=True),

            Text(f'Visualiser Settings', 50, 500, 170, 30, align='centre'),
            Text(f'Grid Size (NxN)', 20, 540, 100, 30, font_size=14, align='left'),
            TextBox(f'{self.grid_size}', 180, 540, 80, 30, font_size=12, border=True, callback=self.callback_grid_size, selectable=True, num_only=True, int_only=True),

        ]
        self.selected_text_box = None

        # PROFILING
        self.profiler = cProfile.Profile()


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                self.profiler.disable()
                # self.profiler.print_stats(sort='cumtime')
            elif event.type == pygame.KEYDOWN:
                # UI interaction
                if self.selected_text_box:
                    if event.key == pygame.K_BACKSPACE:
                        if len(self.selected_text_box.user_text) > 0:
                            self.selected_text_box.user_text = self.selected_text_box.user_text[:-1]
                            continue
                    elif event.key == pygame.K_RETURN:
                        self.selected_text_box.use()
                        continue
                    elif event.key == pygame.K_ESCAPE:
                        self.selected_text_box.reset_selection()
                        continue
                    else:
                        self.selected_text_box.user_text += event.unicode
                        continue

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    self.profiler.disable()
                    continue
                    # self.profiler.print_stats(sort='cumtime')

                elif event.key == pygame.K_SPACE:
                    if self.sort_toggle:
                        np.random.shuffle(self.grid)
                    self.sort_toggle = not self.sort_toggle
                    continue

            elif event.type == pygame.MOUSEBUTTONUP:
                clicked_selectable = False

                if event.button == 1:
                    for element in self.ui_elements:
                        if element.check_clicked(event.pos):

                            element.click()
                            if element.selectable:
                                clicked_selectable = True
                                self.selected_text_box = element

                if not clicked_selectable:
                    self.selected_text_box = None


    def run(self):
        self.profiler.enable()

        for i in range(STARTING_INFECTIONS):
            self.virus_spread_projection.population.people[i].infect()

        while self.day <= self.day_limit:
            self.clock.tick(FPS)
            self.events()
            self.handle_UI()

            if not self.virus_spread_projection.finished:
                if not self.paused:
                    if self.day_has_passed():
                        if SCALE_ANIM_WITH_TIME and self.animate_nodes:
                            if self.day < TIMED_DAYS:
                                start = pygame.time.get_ticks()
                                self.daily_stats[self.day] = self.virus_spread_projection.pass_day(self.day, print_stats=False)
                                runtime = pygame.time.get_ticks() - start

                                self.disease_algorithm_runtime = (self.disease_algorithm_runtime + runtime) // 2
                                self.update_node_animation_time()

                        self.daily_stats[self.day] = self.virus_spread_projection.pass_day(self.day, print_stats=False)

                        # self.write_daily_stats_to_file()

                        self.nodes_update()
                        self.day += 1

            self.draw()


    def draw(self):
        self.screen.fill(BG_COLOUR)

        self.draw_grid()
        self.draw_UI()
        self.nodes_updated_since_draw = False

        self.screen.blit(
            self.grid_surf,
            (((SCREEN_WIDTH // 2) - (self.grid_surf.get_width() // 2)) + 100,
             (SCREEN_HEIGHT // 2) - (self.grid_surf.get_height() // 2))
        )

        self.screen.blit(self.UI_surf, (0, 0))

        pygame.display.update()


    def draw_grid(self):
        self.grid_surf.fill((0, 0, 0))

        if self.sort_toggle and self.nodes_updated_since_draw:
            self.nodes_sort()

        node_index = 0

        for y in range(self.grid_size):
            for x in range(self.grid_size):

                if not self.sort_toggle:
                    node_surf = self.grid[node_index].draw()
                    self.grid_surf.blit(node_surf, (x * self.node_size, y * self.node_size))
                else:
                    node_surf = self.grid_sorted[node_index].draw(no_anim=True)
                    self.grid_surf.blit(node_surf, (x * self.node_size, y * self.node_size))

                node_index += 1


    def draw_UI(self):
        self.UI_surf.fill((0, 0, 0, 0))

        if self.nodes_updated_since_draw:
            self.day_text = self.day_font.render(f'Day: {self.day}', 1, (255, 255, 255))

        for button in self.ui_elements:
            button.draw(self.UI_surf)

        self.UI_surf.blit(self.day_text, (SCREEN_WIDTH // 2 - self.day_text.get_width() // 2, 20))


    def day_has_passed(self):
        if pygame.time.get_ticks() > self.time_count + self.time_step:
            self.time_count = pygame.time.get_ticks()
            return True
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

        node_index = 0
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                node = self.grid[node_index]
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

                node_index += 1

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
            excess_node_count = round((self.nodes[node]['percentage'] - spread_percent) / 100 * self.node_count)

            if excess_node_count > 0:
                if not self.sort_toggle:
                    self.nodes['total']['excess'] += random.sample(self.nodes[node]['nodes'], excess_node_count)
                else:
                    self.nodes['total']['excess'] += self.nodes[node]['nodes'][:excess_node_count]
            elif excess_node_count < 0:
                self.nodes[node]['needed'] = round((spread_percent - self.nodes[node]['percentage']) / 100 * self.node_count)


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
        self.grid_sorted = np.array(sorted(self.grid, reverse=True))


    def write_daily_stats_to_file(self):
        with open(f'./daily_stats.txt', mode='w') as f:
            for key, value in self.daily_stats.items():
                f.write(f'-----------------------------\n')
                f.write(f'Day: {key}\n')

                for k, v in value.items():
                    f.write(f'{k} - {v}\n')

                f.write('\n')


    def update_node_animation_time(self, time=0):
        for node in self.grid:
            node.colour_shift_max_step = 255 * FPS // (self.disease_algorithm_runtime + self.time_step) // 5
            # node.colour_shift_max_step = 5


    def handle_UI(self):
        mpos = pygame.mouse.get_pos()

        for button in self.ui_elements:
            button.update(mpos)


    def reset_UI_elements(self, *exclusions):
        for element in [element for element in self.ui_elements if element not in exclusions]:
            element.reset_selection()


    def callback_pause(self, caller):
        self.paused = not self.paused

    def callback_reset(self, caller):
        self.grid = np.array([Node() for _ in range(self.grid_size ** 2)])
        self.grid_sorted = np.array([Node() for _ in range(self.grid_size ** 2)])
        self.sort_toggle = False
        self.nodes_updated_since_draw = True

        self.virus_spread_projection = VirusSpreadProjection(self.virus_manager.active_virus)
        self.day_limit = DAY_LIMIT
        self.day = 0
        self.daily_stats = {}
        self.nodes = {
            'healthy': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'infected': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'recovered': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'dead': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'total': {'nodes': [], 'excess': []}
        }

        if not self.paused:
            self.ui_elements[0].click()

        self.reset_UI_elements(caller)
        self.run()

    def callback_diagnose_days(self, caller, days):
        new_virus = self.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.diagnose_days = days
        self.virus_manager.active_virus = new_virus

        self.selected_text_box = None
        self.callback_reset(None)

    def callback_recovery_days(self, caller, days):
        new_virus = self.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.recovery_days = days
        self.virus_manager.active_virus = new_virus

        self.selected_text_box = None
        self.callback_reset(None)

    def callback_infection_chance(self, caller, chance):
        new_virus = self.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.infection_chance = chance
        self.virus_manager.active_virus = new_virus

        self.selected_text_box = None
        self.callback_reset(None)

    def callback_reinfection_chance(self, caller, chance):
        new_virus = self.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.reinfection_chance = chance
        self.virus_manager.active_virus = new_virus

        self.selected_text_box = None
        self.callback_reset(None)

    def callback_fatality_chance(self, caller, chance):
        new_virus = self.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.fatality_chance = chance
        self.virus_manager.active_virus = new_virus

        self.selected_text_box = None
        self.callback_reset(None)

    def callback_grid_size(self, caller, num):
        self.grid_size = num
        self.node_count = self.grid_size * self.grid_size
        self.node_size = VIS_WINDOW_SIZE // self.grid_size

        self.grid = np.array([Node() for _ in range(num ** 2)])
        self.grid_sorted = np.array([Node() for _ in range(num ** 2)])

        self.selected_text_box = None
        self.callback_reset(None)