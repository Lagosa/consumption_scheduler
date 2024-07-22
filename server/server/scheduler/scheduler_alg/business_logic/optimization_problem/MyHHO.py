import sys
import random
import numpy as np
import math

from typing import List
from mealpy import HHO
from mealpy.utils.agent import Agent
from ..operations import ConstraintOperations


class MyHHO(HHO.OriginalHHO):
    def __init__(self, building_configuration, **kwargs):
        HHO.OriginalHHO.__init__(self, **kwargs)
        self.building_configuration = building_configuration
        self.best_agent_history = []
        self.current_chaotic_map_value = random.random()
        self.theta = 2.5
        self.K = 5

    def amend_solution(self, solution: np.ndarray) -> np.ndarray:
        usage_matrix = self.building_configuration.usage_matrix
        constraint_matrix = self.building_configuration.constraint_matrix
        solution = ConstraintOperations.apply_constraints(solution, usage_matrix, constraint_matrix)
        return solution

    def update_best_agent_history(self, current_best):
        current_best_fitness = current_best.target.fitness

        if len(self.best_agent_history) == 0:
            self.best_agent_history.append(current_best)
            return

        previous_best_fitness = self.best_agent_history[len(self.best_agent_history) - 1].target.fitness
        if current_best_fitness != previous_best_fitness:
            self.best_agent_history.append(current_best)

    def track_optimize_step(self, pop: List[Agent] = None, epoch: int = None, runtime: float = None) -> None:
        super().track_optimize_step(pop, epoch, runtime)

        sorted_pop = self.get_sorted_population(pop, self.problem.minmax)
        c_best, _ = sorted_pop[0], sorted_pop[-1]

        self.update_best_agent_history(c_best)

    # https://www.mdpi.com/2227-7390/11/19/4181
    def chaotic_map_value(self):
        # self.current_chaotic_map_value = self.get_circle_map_value()
        # return self.current_chaotic_map_value
        return 1

    def get_circle_map_value(self):
        return self.current_chaotic_map_value + self.theta - ((self.K * 1.0 / (2 * math.pi))
                                                              * math.sin(2 * math.pi * self.current_chaotic_map_value)) % 1

    def generate_empty_agent(self, solution: np.ndarray = None) -> Agent:
        if solution is None:
            solution = self.problem.generate_solution(encoded=True) * self.chaotic_map_value()
        return Agent(solution=solution)

    def evolve(self, epoch):
        """
        The main operations (equations) of algorithm. Inherit from Optimizer class

        Args:
            epoch (int): The current iteration
        """
        pop_new = []
        for idx in range(0, self.pop_size):
            # -2 < E0 < 2
            E0 = 4 * self.generator.uniform() - 2
            # factor to show the decreasing energy of rabbit
            E = 2 * self.chaotic_map_value() * E0 * (1. - epoch * 1.0 / self.epoch)
            J = 2 * (1 - self.generator.uniform())

            # -------- Exploration phase Eq. (1) in paper -------------------
            if np.abs(E) >= 1:
                # Harris' hawks perch randomly based on 2 strategy:
                if self.generator.random() >= 0.5:  # perch based on other family members
                    X_rand = self.pop[self.generator.integers(0, self.pop_size)].solution.copy()
                    pos_new = X_rand - self.chaotic_map_value() * self.generator.uniform() * np.abs(
                        X_rand - 2 * self.chaotic_map_value() * self.generator.uniform() * self.pop[idx].solution)
                else:  # perch on a random tall tree (random site inside group's home range)
                    X_m = np.mean([x.solution for x in self.pop])
                    pos_new = (self.g_best.solution - X_m) - self.chaotic_map_value() * self.generator.uniform() * \
                              (self.problem.lb + self.chaotic_map_value() * self.generator.uniform() * (self.problem.ub - self.problem.lb))
                pos_new = self.correct_solution(pos_new)
                agent = self.generate_empty_agent(pos_new)
                pop_new.append(agent)
            # -------- Exploitation phase -------------------
            else:
                # Attacking the rabbit using 4 strategies regarding the behavior of the rabbit
                # phase 1: ----- surprise pounce (seven kills) ----------
                # surprise pounce (seven kills): multiple, short rapid dives by different hawks
                if (self.generator.random() >= 0.5):
                    delta_X = self.g_best.solution - self.pop[idx].solution
                    if np.abs(E) >= 0.5:  # Hard besiege Eq. (6) in paper
                        pos_new = delta_X - E * np.abs(J * self.g_best.solution - self.pop[idx].solution)
                    else:  # Soft besiege Eq. (4) in paper
                        pos_new = self.g_best.solution - E * np.abs(delta_X)
                    pos_new = self.correct_solution(pos_new)
                    agent = self.generate_empty_agent(pos_new)
                    pop_new.append(agent)
                else:
                    LF_D = self.get_levy_flight_step(beta=1.5, multiplier=0.01, case=-1)
                    if np.abs(E) >= 0.5:  # Soft besiege Eq. (10) in paper
                        Y = self.g_best.solution - E * np.abs(J * self.g_best.solution - self.pop[idx].solution)
                    else:  # Hard besiege Eq. (11) in paper
                        X_m = np.mean([x.solution for x in self.pop])
                        Y = self.g_best.solution - E * np.abs(J * self.g_best.solution - X_m)
                    pos_Y = self.correct_solution(Y)
                    target_Y = self.get_target(pos_Y)
                    Z = Y + self.generator.uniform(self.problem.lb, self.problem.ub) * LF_D
                    pos_Z = self.correct_solution(Z)
                    target_Z = self.get_target(pos_Z)
                    if self.compare_target(target_Y, self.pop[idx].target, self.problem.minmax):
                        agent = self.generate_empty_agent(pos_Y)
                        agent.target = target_Y
                        pop_new.append(agent)
                        continue
                    if self.compare_target(target_Z, self.pop[idx].target, self.problem.minmax):
                        agent = self.generate_empty_agent(pos_Z)
                        agent.target = target_Z
                        pop_new.append(agent)
                        continue
                    pop_new.append(self.pop[idx].copy())
            # chaotic_solution = pop_new[-1].solution + random.random() * (self.g_best.solution - self.pop[idx].solution)
            # chaotic_solution_fitness = self.get_target(chaotic_solution).fitness
            # solution_fitness = self.get_target(pop_new[-1].solution).fitness
            # if chaotic_solution_fitness < solution_fitness:
            #     pop_new[-1].solution = chaotic_solution

        if self.mode not in self.AVAILABLE_MODES:
            for idx, agent in enumerate(pop_new):
                pop_new[idx].target = self.get_target(agent.solution)
        else:
            pop_new = self.update_target_for_population(pop_new)
        self.pop = self.greedy_selection_population(self.pop, pop_new, self.problem.minmax)
