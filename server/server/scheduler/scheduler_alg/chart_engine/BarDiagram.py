import matplotlib.pyplot as plt


def drawBarDiagram(chart_details):
    plt.bar(chart_details["x_label_values"], chart_details["data_array"], color="#415688", width=0.7)

    plt.xticks(range(len(chart_details["x_label_values"])), chart_details["x_label_values"])
    plt.grid(True)
    plt.xlabel(chart_details["x_label"])
    plt.ylabel(chart_details["y_label"])
    plt.title(chart_details["plot_name"])
    plt.legend(chart_details["row_label_values"])

    plt.savefig("charts/" + chart_details["plot_file_name"] + ".png")
    plt.show()

