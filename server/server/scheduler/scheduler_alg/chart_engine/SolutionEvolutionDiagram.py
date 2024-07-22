import os.path
import imageio.v2 as imageio
import numpy as np

from . import EvaluationDiagrams


def drawEvolutionDiagram(consumption, schedule_evolution, target_curve):
    if not os.path.exists("charts/temp"):
        os.makedirs("charts/temp")

    for index, solution in enumerate(schedule_evolution):
        drawFrame(consumption, solution, target_curve, index)

    gif = build_gif(schedule_evolution)
    imageio.mimsave("charts/approximation_evolution.gif", gif, fps=2, loop=0)


def drawFrame(consumption, schedule, target_curve, index):
    EvaluationDiagrams.compareTotalConsumptionAndTarget(consumption, schedule, target_curve,
                                                        f"charts/temp/solution_evolution_{index}.png",
                                                        do_show_diagram=False)


def build_gif(schedule_evolution):
    gif = []

    if len(schedule_evolution) <= 0:
        return gif

    initial_frame = imageio.imread("charts/temp/solution_evolution_0.png")
    blank_img_array = np.ones(initial_frame.shape, dtype="uint8")
    imageio.imwrite("charts/temp/blank_img.png", blank_img_array * 255)
    gif.append(imageio.imread("charts/temp/blank_img.png"))

    for index in range(len(schedule_evolution)):
        frame = imageio.imread(f"charts/temp/solution_evolution_{index}.png")
        gif.append(frame)
    return gif
