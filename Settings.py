DAY_LIMIT = 500

# Population
POPULATION_SIZE = 100000
CONTACTS_PER_DAY_UNKNOWN_CARRIER = 4
CONTACTS_PER_DAY_KNOWN = 1

# Disease
DIAGNOSE_DAYS = 14
RECOVERY_DAYS = 30
INFECTION_CHANCE = 3.27   # percentage (R0 / RNaught)
SECONDARY_INFECTION_CHANCE = 3.27    # percentage
FATALITY_RATE = 1   # percentage

# Graphing
SAVE_LOCATION = './Figures/'

"""
80% mild case
20% hospitalisation
3-5% ICU

Mainland China R0 = 2.79
Australia - 3.27
Global mean - 3.28
Global median - 2.79
"""