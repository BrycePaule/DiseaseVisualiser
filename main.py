from statistics import mean

from GeneticAlgorithm import GeneticAlgorithm


def run_old():
    generations_list = []
    best_list = []
    lines = [' ']

    for i in range(100):
        demo = GeneticAlgorithm()
        generations, best = demo.run()

        generations_list.append(generations)
        best_list.append(best.fitness)

        lines.append(f'Generations: {generations} - Fittest: {best.fitness}')

    with open('results.txt', mode='w') as f:
        lines[
            0] = f'Generations AVG: {mean(generations_list)}  -  Fitness AVG: {mean(best_list)}'

        for line in lines:
            f.write(f'{line}\n')


def run_in_100_blocks(times):
    results = []

    for n in range(times):
        generations_list = []
        best_list = []

        for i in range(100):
            print(f'Block {n}: {i}')
            demo = GeneticAlgorithm()
            generations, best = demo.run()

            generations_list.append(generations)
            best_list.append(best.fitness)
            print(f'    - (G: {generations}, F: {best.fitness})')

        results.append(f'{mean(generations_list)}   {mean(best_list)}')

    with open('results.txt', mode='w') as f:
        for line in results:
            f.write(f'{line}\n')


run_in_100_blocks(10)