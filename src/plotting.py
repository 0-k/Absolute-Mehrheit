import matplotlib.pyplot as plt
import math

from simulation import Simulation
import parties
import coalitions


def plot_coalitions(simulation):
    rows = 2
    columns = int(math.ceil(len(coalitions.ALL) / rows))
    fig, axs = plt.subplots(rows, columns)
    idx = 0
    for coalition in coalitions.ALL:
        seats_by_coalition = simulation.evaluate_seats_by(coalition)
        plot_idx = idx // columns, idx % columns
        axs[plot_idx].hist(seats_by_coalition, bins=10, color='black')
        axs[plot_idx].set_title(coalition.name)
        axs[plot_idx].set_xlim(151, 450)
        axs[plot_idx].axvline(300, color='red', linestyle='--')
        idx += 1
    plt.show()


if __name__ == '__main__':
    sim = Simulation(parties.ALL)
    plot_coalitions(sim)

