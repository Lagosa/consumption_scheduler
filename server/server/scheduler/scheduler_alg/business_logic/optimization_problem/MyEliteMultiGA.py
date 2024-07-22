from mealpy.evolutionary_based.GA import EliteMultiGA


class MyEliteMultiGA(EliteMultiGA):

    def __init__(self, epoch_number, population_size, crossover_probability, mutation_probability, **kwargs):
        super().__init__(epoch=epoch_number, pop_size=population_size,
                         pc=crossover_probability, pm=mutation_probability, **kwargs)
