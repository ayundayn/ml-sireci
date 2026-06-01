import random

from app.recommenders.itinerary_simulator import (
    ItinerarySimulator
)


class GeneticAlgorithm:

    def __init__(
        self,
        df_places,
        df_kuliner,
        df_jarak,
        df_waktu,
        total_days=1,
        max_budget=1000000,
        start_time="08:00",
        end_time="20:00",
        ngen=50,
        popsize=30
    ):

        self.df_places = df_places
        self.df_kuliner = df_kuliner

        self.simulator = ItinerarySimulator(
            df_places=df_places,
            df_kuliner=df_kuliner,
            df_jarak=df_jarak,
            df_waktu=df_waktu,
            total_days=total_days,
            max_budget=max_budget,
            start_time=start_time,
            end_time=end_time
        )

        self.ngen = ngen
        self.popsize = popsize

    def fitness(self, order):

        return self.simulator.simulate(order)

    def tournament_selection(self, pop, fits, k=3):

        selected = random.sample(range(len(pop)), k)

        best = max(
            selected,
            key=lambda i: fits[i][1][1]
        )

        return pop[best]

    def ordered_crossover(self, p1, p2):

        if len(p1) < 2:
            return p1
    
        a, b = sorted(
            random.sample(range(len(p1)), 2)
        )

        child = [None] * len(p1)

        child[a:b] = p1[a:b]

        fill = [x for x in p2 if x not in child]

        j = 0

        for i in range(len(child)):

            if child[i] is None:

                child[i] = fill[j]

                j += 1

        return child

    def mutate(self, order, rate=0.2):

        order = order[:]

        for i in range(len(order)):

            if random.random() < rate:

                j = random.randint(
                    0,
                    len(order) - 1
                )

                order[i], order[j] = (
                    order[j],
                    order[i]
                )

        return order

    def run(self):

        n = len(self.df_places)

        population = [

            random.sample(range(n), n)

            for _ in range(self.popsize)

        ]

        best_solution = None
        best_fitness = -999

        for _ in range(self.ngen):

            fits = [

                (ind, self.fitness(ind))

                for ind in population

            ]

            fits_sorted = sorted(
                fits,
                key=lambda x: x[1][1],
                reverse=True
            )

            current_best = fits_sorted[0]

            if current_best[1][1] > best_fitness:

                best_solution = current_best[1]

                best_fitness = current_best[1][1]

            new_population = []

            # elitism
            elites = fits_sorted[:5]

            new_population.extend(
                [e[0] for e in elites]
            )

            while len(new_population) < self.popsize:

                p1 = self.tournament_selection(
                    population,
                    fits
                )

                p2 = self.tournament_selection(
                    population,
                    fits
                )

                child = self.ordered_crossover(
                    p1,
                    p2
                )

                child = self.mutate(child)

                new_population.append(child)

            population = new_population

        return best_solution