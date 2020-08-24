from Settings.VisualiserSettings import HEALTHY, INFECTED_UNKNOWN, INFECTED_KNOWN, RECOVERED, DEAD

def colour_lookup(state):
    colours = {
        0: HEALTHY,
        1: INFECTED_UNKNOWN,
        2: INFECTED_KNOWN,
        3: RECOVERED,
        4: DEAD,
    }

    return colours[state]