import matplotlib.pyplot as plt


def draw_diagram(plot, i, chart_details):
    plot[i].pie(chart_details["data_array"], colors=chart_details["colors"],  autopct='%1.1f%%', pctdistance=0.85, wedgeprops=dict(width=0.3))
    plot[i].set_title(chart_details["title"])

    plot[i].legend(chart_details["labels"], loc="lower center", bbox_to_anchor=(0.5, -0.3))
