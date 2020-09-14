from copy import deepcopy

class Virus:

    def __init__(self, name, diagnose_days, recovery_days, infection_chance, reinfection_chance, fatality_chance):
        self.name = name
        self.diagnose_days = diagnose_days
        self.recovery_days = recovery_days
        self.infection_chance = infection_chance
        self.reinfection_chance = reinfection_chance
        self.fatality_chance = fatality_chance


    def dict(self):
        return {
            'name': self.name,
            'diagnose_days': self.diagnose_days,
            'recovery_days': self.recovery_days,
            'infection_chance': self.infection_chance,
            'reinfection_chance': self.reinfection_chance,
            'fatality_chance': self.fatality_chance
        }

    def copy(self):
        return deepcopy(self)


    def __repr__(self):
        return f'<Virus: {self.name}>'