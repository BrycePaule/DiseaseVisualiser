import numpy as np

from Visualiser.Node import Node

from SpreadProjection.VirusSpreadProjection import VirusSpreadProjection

from Settings.VisualiserSettings import VIS_WINDOW_SIZE


class CallbackManager:

    def __init__(self, visualiser):
        self.visualiser = visualiser
        self.callbacks = {
            'pause': self.callback_pause,
            'reset': self.callback_reset,

            'select_virus': self.callback_select_virus,
            'diagnosis': self.callback_diagnose_days,
            'recovery': self.callback_recovery_days,
            'infection': self.callback_infection_chance,
            'reinfection': self.callback_reinfection_chance,
            'fatality': self.callback_fatality_chance,

            'grid_size': self.callback_grid_size,
            'time_step': self.callback_time_step,

            'pop_size': self.callback_pop_size,
            'starting_infections': self.callback_starting_infections,
            'contacts_undiagnosed': self.callback_contacts_undiagnosed,
            'contacts_diagnosed': self.callback_contacts_diagnosed,
        }


    def callback_pause(self, *args):
        self.visualiser.paused = not self.visualiser.paused


    def callback_reset(self, *args):
        self.visualiser.grid = np.array([Node(border=self.visualiser.node_border, animate=self.visualiser.animate_nodes) for _ in range(self.visualiser.grid_size ** 2)])
        self.visualiser.grid_sorted = np.array([Node(border=self.visualiser.node_border, animate=self.visualiser.animate_nodes) for _ in range(self.visualiser.grid_size ** 2)])
        self.visualiser.sort_toggle = False
        self.visualiser.nodes_updated_since_draw = True

        self.visualiser.virus_spread_projection = VirusSpreadProjection(self.visualiser.virus_manager.active_virus, self.visualiser.projection_settings)
        self.visualiser.day = 0
        self.visualiser.daily_stats = {}
        self.visualiser.nodes = {
            'healthy': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'infected': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'recovered': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'dead': {'nodes': [], 'percentage': 0.00, 'excess': 0, 'needed': 0},
            'total': {'nodes': [], 'excess': []}
        }

        virus_setting_fields = [element for element in self.visualiser.ui_elements if element.tag == 'virus_setting']
        virus_setting_fields[0].text = f'{self.visualiser.virus_manager.active_virus.diagnose_days}'
        virus_setting_fields[0].render_text()
        virus_setting_fields[1].text = f'{self.visualiser.virus_manager.active_virus.recovery_days}'
        virus_setting_fields[1].render_text()
        virus_setting_fields[2].text = f'{self.visualiser.virus_manager.active_virus.infection_chance}'
        virus_setting_fields[2].render_text()
        virus_setting_fields[3].text = f'{self.visualiser.virus_manager.active_virus.reinfection_chance}'
        virus_setting_fields[3].render_text()
        virus_setting_fields[4].text = f'{self.visualiser.virus_manager.active_virus.fatality_chance}'
        virus_setting_fields[4].render_text()

        if not self.visualiser.paused:
            self.visualiser.ui_elements[0].click()

        self.visualiser.run()


    def callback_diagnose_days(self, *args):
        try:
            days = args[0]
        except ValueError:
            return

        new_virus = self.visualiser.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.diagnose_days = days
        self.visualiser.virus_manager.active_virus = new_virus

        self.visualiser.selected_text_box = None
        self.callback_reset()


    def callback_recovery_days(self, *args):
        try:
            days = args[0]
        except ValueError:
            return

        new_virus = self.visualiser.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.recovery_days = days
        self.visualiser.virus_manager.active_virus = new_virus

        self.visualiser.selected_text_box = None
        self.callback_reset()


    def callback_infection_chance(self, *args):
        try:
            chance = args[0]
        except ValueError:
            return

        new_virus = self.visualiser.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.infection_chance = chance
        self.visualiser.virus_manager.active_virus = new_virus

        self.visualiser.selected_text_box = None
        self.callback_reset()


    def callback_reinfection_chance(self, *args):
        try:
            chance = args[0]
        except ValueError:
            return

        new_virus = self.visualiser.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.reinfection_chance = chance
        self.visualiser.virus_manager.active_virus = new_virus

        self.visualiser.selected_text_box = None
        self.callback_reset()


    def callback_fatality_chance(self, *args):
        try:
            chance = args[0]
        except ValueError:
            return

        new_virus = self.visualiser.virus_manager.active_virus.copy()
        new_virus.name = 'Custom'
        new_virus.fatality_chance = chance
        self.visualiser.virus_manager.active_virus = new_virus

        self.visualiser.selected_text_box = None
        self.callback_reset()


    def callback_grid_size(self, *args):
        try:
            num = args[0]
        except ValueError:
            return

        self.visualiser.grid_size = num
        if num > 200:
            self.visualiser.node_border = False
            self.visualiser.animate_nodes = False
        else:
            self.visualiser.node_border = True
            self.visualiser.animate_nodes = True

        self.visualiser.node_count = self.visualiser.grid_size * self.visualiser.grid_size
        self.visualiser.node_size = VIS_WINDOW_SIZE // self.visualiser.grid_size

        self.visualiser.selected_text_box = None
        self.callback_reset()


    def callback_time_step(self, *args):
        try:
            num = args[0]
        except ValueError:
            return

        self.visualiser.time_step = num

        self.visualiser.selected_text_box = None
        self.callback_reset()


    def callback_select_virus(self, *args):
        try:
            virus = args[0]
        except ValueError:
            return

        self.visualiser.virus_manager.active_virus = self.visualiser.virus_manager.diseases[virus]
        self.callback_reset()


    def callback_pop_size(self, *args):
        try:
            pop_size = args[0]
        except ValueError:
            return

        if pop_size > 10000:
            self.visualiser.animate_nodes = False
        else:
            self.visualiser.animate_nodes = True


        self.visualiser.projection_settings.pop_size = pop_size
        self.callback_reset()


    def callback_starting_infections(self, *args):
        try:
            starting_infections = args[0]
        except ValueError:
            return

        self.visualiser.projection_settings.starting_infections = starting_infections
        self.callback_reset()


    def callback_contacts_undiagnosed(self, *args):
        try:
            contacts = args[0]
        except ValueError:
            return

        self.visualiser.projection_settings.contacts_undiag = contacts
        self.callback_reset()


    def callback_contacts_diagnosed(self, *args):
        try:
            contacts = args[0]
        except ValueError:
            return

        self.visualiser.projection_settings.contacts_diag = contacts
        self.callback_reset()