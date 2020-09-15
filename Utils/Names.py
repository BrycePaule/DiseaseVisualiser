import random
import numpy as np

names = []
with open('./Utils/names.txt', mode='r') as f:
    for line in f:
        names.append(line.strip())
    names = np.array(names)

def get_random_name():
    return names[random.randrange(0, names.size)]