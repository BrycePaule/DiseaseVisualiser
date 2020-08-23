import random

names = []
with open('./names.txt', mode='r') as f:
    for line in f:
        names.append(line.strip())

def get_random_name():
    return names[random.randrange(0, len(names))]