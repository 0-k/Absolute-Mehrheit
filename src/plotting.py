import numpy as np

from bokeh.layouts import gridplot
from bokeh.plotting import figure, output_file, show


def make_plot(title, hist, edges):
    p = figure(title=title, tools='', background_fill_color="#fafafa")
    p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
           fill_color="#E71D36", line_color="black", alpha=0.8)
    p.y_range.start = 0
    p.xaxis.axis_label = 'x'
    p.yaxis.axis_label = 'Pr(x)'
    p.grid.grid_line_color = "white"
    return p

def normal_distribution(mu, sigma):
    measured = np.random.normal(mu, sigma, 1000)
    hist, edges = np.histogram(measured, density=True, bins=50)
    return make_plot("Coalition (μ={}, σ={})".format(str(mu), str(sigma)), hist, edges)


p1 = normal_distribution(0, 0.5)
p2 = normal_distribution(1, 1.0)
p3 = normal_distribution(2, 0.5)
p4 = normal_distribution(-1, 2.5)


output_file('../results/sample_histogram.html', title="histogram.py example")

show(gridplot([p1, p2, p3, p4], ncols=2, plot_width=400, plot_height=400, toolbar_location=None))