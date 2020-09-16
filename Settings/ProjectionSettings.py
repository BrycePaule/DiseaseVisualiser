
# Population
POPULATION_SIZE = 10000
STARTING_INFECTIONS = 1
CONTACTS_PER_DAY_UNKNOWN_CARRIER = 4
CONTACTS_PER_DAY_KNOWN = 1
DAY_LIMIT = 10000


# Disease
"""
COVID-19
80% mild case
20% hospitalisation
3-5% ICU

Mainland China R0 = 2.79
Australia - 3.27
Global mean - 3.28
Global median - 2.79
"""

DIAGNOSE_DAYS = 14
RECOVERY_DAYS = 30
INFECTION_CHANCE = 3.27   # percentage (R0 / RNaught)
SECONDARY_INFECTION_CHANCE = 0    # percentage
FATALITY_RATE = 1   # percentage


# Graphing
SAVE_LOCATION = './Outputs/Figures/'
SAVE_PREFIX = 0
with open('./Settings/graph_prefix_inc.txt', 'r') as f:
    for line in f:
        SAVE_PREFIX = int(line.strip())

with open('./Settings/graph_prefix_inc.txt', 'w') as f:
    f.write(f'{SAVE_PREFIX + 1}')


