import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def drawLineDiagram(chart_details, show=True):
    if not is_row_label_values_valid(chart_details["data_array"], chart_details["row_label_values"]):
        print("Invalid row label values array!")
        return
    colors = ["b","g","g"]
    for i, row in enumerate(chart_details["data_array"]):
        plt.plot(row, label=chart_details["row_label_values"][i], color=colors[i])

    plt.xticks(range(len(chart_details["x_label_values"])), chart_details["x_label_values"])
    plt.grid(True)
    plt.xlabel(chart_details["x_label"])
    plt.ylabel(chart_details["y_label"])
    plt.title(chart_details["plot_name"])
    plt.xticks(range(0,21, 1), range(0, 21, 1))
    plt.legend()

    plt.savefig(chart_details["plot_file_name"])
    if show:
        plt.show()
    plt.close()



def is_row_label_values_valid(data_array, row_label_values):
    data_array_rows, data_array_columns = np.array(data_array).shape
    return True if data_array_rows == len(row_label_values) else False
