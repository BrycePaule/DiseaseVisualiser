import pygame
import random
import numpy as np
import cProfile

from Visualiser.Node import Node

from SpreadProjection.VirusSpreadProjection import VirusSpreadProjection
from SpreadProjection.VirusManager import VirusManager
from Settings.ProjectionSettingsPackage import ProjectionSettingsPackage

from Settings.VisualiserSettings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from Settings.VisualiserSettings import VIS_WINDOW_SIZE, VIS_NODE_WIDTH
from Settings.VisualiserSettings import MIN_ALGORITHM_CALL_STEP, TIMED_DAYS, ANIMATE_NODES, NODE_BORDER
from Settings.VisualiserSettings import BG_COLOUR, SCALE_ANIM_WITH_TIME
from Settings.ProjectionSettings import DAY_LIMIT

from Visualiser.UI.UIElements.Button import Button
from Visualiser.UI.UIElements.TextBox import TextBox
from Visualiser.UI.UIElements.Text import Text
from Visualiser.CallbackManager import CallbackManager


class Visualiser:

    pygame.init()
    pygame.font.init()
    pygame.display.set_caption('Virus Spread Visualiser')

    def __init__(self):
        # VISUALISER SETTINGS
        self.time_step = MIN_ALGORITHM_CALL_STEP   # 1000ms = 1s
        self.time_count = pygame.time.get_ticks()
        self.node_border = NODE_BORDER
        self.animate_nodes = ANIMATE_NODES

        self.disease_algorithm_runtime = 0

        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.grid_surf = pygame.Surface((VIS_WINDOW_SIZE, VIS_WINDOW_SIZE))
        self.UI_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)

        self.day_font = pygame.font.SysFont('Arial', 30)
        self.day_text = None
        self.CBM = CallbackManager(self)

        self.paused = True

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
        self.projection_settings = ProjectionSettingsPackage()
        self.virus_spread_projection = VirusSpreadProjection(self.virus_manager.diseases['COVID-19'], self.projection_settings)
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

        self.ui_elements = self.build_UI()
        self.selected_text_box = None

        # PROFILING
        self.profiler = cProfile.Profile()


    """ SETUP """
    def build_UI(self):
        ui_elements = []

        ui_elements.append(Button('Start', 20, 110, 100, 30, tag='runtime', border=True, hover_colour=(128, 185, 105), callback=self.CBM.callbacks['pause'], toggleable=True, alt_text='Pause'))
        ui_elements.append(Button('Reset', 140, 110, 100, 30, tag='runtime', border=True, hover_colour=(200, 90, 90), callback=self.CBM.callbacks['reset']))

        ui_elements.append(Text(f'Virus', 65, 170, 130, 30, align='centre'))
        for button in self.create_virus_buttons():
            ui_elements.append(button)

        ui_elements.append(Text(f'Virus Settings', 65, 300, 130, 30, align='centre'))
        ui_elements.append(Text(f'Diagnosis Time', 20, 340, 115, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.virus_manager.active_virus.diagnose_days}', 180, 340, 80, 30, tag='virus_setting', font_size=12, text_suffix=' (days)', border=True, callback=self.CBM.callbacks['diagnosis'], selectable=True, num_only=True))
        ui_elements.append(Text(f'Recovery Time', 20, 375, 110, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.virus_manager.active_virus.recovery_days}', 180, 375, 80, 30, tag='virus_setting', font_size=12, text_suffix=' (days)', border=True, callback=self.CBM.callbacks['recovery'], selectable=True, num_only=True))
        ui_elements.append(Text(f'Infection Chance', 20, 410, 120, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.virus_manager.active_virus.infection_chance}', 180, 410, 80, 30, tag='virus_setting', font_size=12, text_suffix='%', border=True, callback=self.CBM.callbacks['infection'], selectable=True, num_only=True))
        ui_elements.append(Text(f'Re-Infection Chance', 20, 445, 150, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.virus_manager.active_virus.reinfection_chance}', 180, 445, 80, 30, tag='virus_setting', font_size=12, text_suffix='%', border=True, callback=self.CBM.callbacks['reinfection'], selectable=True, num_only=True))
        ui_elements.append(Text(f'Fatality Rate', 20, 480, 100, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.virus_manager.active_virus.fatality_chance}', 180, 480, 80, 30, tag='virus_setting', font_size=12, text_suffix='%', border=True, callback=self.CBM.callbacks['fatality'], selectable=True, num_only=True))

        ui_elements.append(Text(f'Projection Settings', 55, 535, 165, 30, align='centre'))
        ui_elements.append(Text(f'Population Size', 20, 575, 100, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.projection_settings.pop_size}', 180, 575, 80, 30, tag='projection_setting', font_size=12, border=True, callback=self.CBM.callbacks['pop_size'], selectable=True, num_only=True, int_only=True))
        ui_elements.append(Text(f'Initial Infections', 20, 610, 120, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.projection_settings.starting_infections}', 180, 610, 80, 30, tag='projection_setting', font_size=12, border=True, callback=self.CBM.callbacks['starting_infections'], selectable=True, num_only=True, int_only=True))
        ui_elements.append(Text(f'Contacts (undiagnosed)', 20, 645, 155, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.projection_settings.contacts_undiag}', 180, 645, 80, 30, tag='projection_setting', font_size=12, text_suffix=' ( p/day)', border=True, callback=self.CBM.callbacks['contacts_undiagnosed'], selectable=True, num_only=True, int_only=True))
        ui_elements.append(Text(f'Contacts (diagnosed)', 20, 680, 140, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.projection_settings.contacts_diag}', 180, 680, 80, 30, tag='projection_setting', font_size=12, text_suffix=' ( p/day)', border=True, callback=self.CBM.callbacks['contacts_diagnosed'], selectable=True, num_only=True, int_only=True))
        ui_elements.append(Text(f'Day Limit', 20, 715, 100, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.day_limit}', 180, 715, 80, 30, tag='projection_setting', font_size=12, border=True, callback=self.CBM.callbacks['day_limit'], selectable=True, num_only=True, int_only=True))

        ui_elements.append(Text(f'Visualiser Settings', 50, 770, 170, 30, align='centre'))
        ui_elements.append(Text(f'Grid Size (NxN)', 20, 820, 100, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.grid_size}', 180, 820, 80, 30, tag='vis_setting', font_size=12, border=True, callback=self.CBM.callbacks['grid_size'], selectable=True, num_only=True, int_only=True))
        ui_elements.append(Text(f'Time Step', 20, 855, 100, 30, font_size=14, align='left'))
        ui_elements.append(TextBox(f'{self.time_step}', 180, 855, 80, 30, tag='vis_setting', font_size=12, text_suffix=' (ms)', border=True, callback=self.CBM.callbacks['time_step'], selectable=True, num_only=True, int_only=True))

        return ui_elements


    def create_virus_buttons(self):
        buttons = []
        left_col = True
        y = 210

        for virus in self.virus_manager.diseases:
            if left_col:
                buttons.append(Button(virus, 20, y, 100, 30, tag='virus', font_size=12, border=True, callback=self.CBM.callbacks['select_virus'], callback_rv='text'))
            else:
                buttons.append(Button(virus, 140, y, 100, 30, tag='virus', font_size=12, border=True, callback=self.CBM.callbacks['select_virus'], callback_rv='text'))
                y += 35

            left_col = not left_col

        return buttons


    """ RUNTIME """
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
                    # self.profiler.print_stats(sort='cumtime')
                    continue

                elif event.key == pygame.K_SPACE:
                    if self.sort_toggle:
                        np.random.shuffle(self.grid)
                    self.sort_toggle = not self.sort_toggle
                    self.nodes_updated_since_draw = True
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
        self.virus_spread_projection.infect_initial()

        while True:
            self.clock.tick(FPS)
            self.events()
            self.update_UI()

            if not self.virus_spread_projection.finished:
                if not self.paused:

                    if self.day >= self.day_limit:
                        self.CBM.callbacks['pause']()

                    if self.check_day_has_passed():
                        if SCALE_ANIM_WITH_TIME and self.animate_nodes:
                            if self.day < TIMED_DAYS:
                                start = pygame.time.get_ticks()
                                self.daily_stats[self.day] = self.virus_spread_projection.pass_day(self.day, print_stats=True)
                                runtime = pygame.time.get_ticks() - start

                                self.disease_algorithm_runtime = (self.disease_algorithm_runtime + runtime) // 2
                                self.update_node_animation_time()

                        self.daily_stats[self.day] = self.virus_spread_projection.pass_day(self.day, print_stats=True)

                        # self.write_daily_stats_to_file()

                        self.nodes_update()
                        self.day += 1


            self.draw()


    def check_day_has_passed(self):
        if pygame.time.get_ticks() > self.time_count + self.time_step:
            self.time_count = pygame.time.get_ticks()
            return True
        return False


    def update_UI(self):
        mpos = pygame.mouse.get_pos()

        for button in self.ui_elements:
            button.update(mpos)


    """ DRAWING """
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


    """ NODE CALCULATIONS"""
    def nodes_update(self):
        self.nodes_tally()
        self.nodes_calc_visualiser_vs_projection_diff()
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


    def nodes_calc_visualiser_vs_projection_diff(self):

        """
        Calculates the difference between the Projection spread, and visualiser
        spread - (there will most likely always be some difference here given
        Visualiser has MUCH less nodes than Projection does people
        """

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


    def update_node_animation_time(self, time=0):
        for node in self.grid:
            node.colour_shift_max_step = 255 * FPS // (self.disease_algorithm_runtime + self.time_step) // 5
            # node.colour_shift_max_step = 5


    """ OUTPUT """
    def write_daily_stats_to_file(self):
        with open(f'./daily_stats.txt', mode='w') as f:
            for key, value in self.daily_stats.items():
                f.write(f'-----------------------------\n')
                f.write(f'Day: {key}\n')

                for k, v in value.items():
                    f.write(f'{k} - {v}\n')

                f.write('\n')