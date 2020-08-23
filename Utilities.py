import random

def roll(chance):

    throw = random.randint(0, 100)

    if throw < chance:
        return True

    return False