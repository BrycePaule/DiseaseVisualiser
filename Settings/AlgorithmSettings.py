
# VISUALISER
DAY_LIMIT = 999999999


# Population
POPULATION_SIZE = 1000
CONTACTS_PER_DAY_UNKNOWN_CARRIER = 2
CONTACTS_PER_DAY_KNOWN = 1


# Disease
"""
80% mild case
20% hospitalisation
3-5% ICU

Mainland China R0 = 2.79
Australia - 3.27
Global mean - 3.28
Global median - 2.79
"""
STARTING_INFECTIONS = 1
DIAGNOSE_DAYS = 14
RECOVERY_DAYS = 30
INFECTION_CHANCE = 3.27   # percentage (R0 / RNaught)
SECONDARY_INFECTION_CHANCE = 0    # percentage
FATALITY_RATE = 1   # percentage


# Graphing
SAVE_LOCATION = './Outputs/Figures/'
SAVE_PREFIX = 0
with open('./Settings/prefix_inc.txt', 'r') as f:
    for line in f:
        SAVE_PREFIX = int(line.strip())

with open('./Settings/prefix_inc.txt', 'w') as f:
    f.write(f'{SAVE_PREFIX + 1}')


