from Settings.ProjectionSettings import POPULATION_SIZE, STARTING_INFECTIONS, CONTACTS_PER_DAY_UNKNOWN_CARRIER, CONTACTS_PER_DAY_KNOWN, DAY_LIMIT

from enum import Enum

class ProjectionSettingsPackage:

    def __init__(self, pop_size=POPULATION_SIZE, starting_infections=STARTING_INFECTIONS,
                    contacts_undiag=CONTACTS_PER_DAY_UNKNOWN_CARRIER, contacts_diag=CONTACTS_PER_DAY_KNOWN):
        self.pop_size = pop_size
        self.starting_infections = starting_infections
        self.contacts_undiag = contacts_undiag
        self.contacts_diag = contacts_diag