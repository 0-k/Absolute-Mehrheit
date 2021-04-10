from simulation import Simulation
import party
import src.coalition as coalition
import matplotlib.pyplot as plt


def plot_coalitions(simulation):
    black_green_result = simulation.evaluate_seats_coalition(coalition.BLACK_RED)

    #black_red_result = simulation.evaluate_seats_coalition(black_red)
    #green_red_red_result = simulation.evaluate_seats_coalition(green_red_red)
    #black_yellow_result = simulation.evaluate_seats_coalition(black_yellow)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].hist(black_green_result, bins=10, color='black')
    axs[0, 0].set_title('Black Green')

    axs[0, 0].set_xlim(151, 450)
    axs[0, 0].axvline(300, color='red', linestyle='--')


    """
    axs[0, 1].hist(black_red_result, bins=10, color='black')
    axs[0, 1].set_title('Black Red')
    axs[1, 0].hist(green_red_red_result, bins=10, color='black')
    axs[1, 0].set_title('Green Red Red')
    axs[1, 1].hist(black_yellow_result, bins=10, color='black')
    axs[1, 1].set_title('Black Yellow')

    axs[0, 1].set_xlim(151, 450)
    axs[1, 0].set_xlim(151, 450)
    axs[1, 1].set_xlim(151, 450)

    axs[0, 1].axvline(300, color='red', linestyle='--')
    axs[1, 0].axvline(300, color='red', linestyle='--')
    axs[1, 1].axvline(300, color='red', linestyle='--')
    """
    plt.show()


if __name__ == '__main__':
    '''**  Try again. Fail again. Fail better. **'''

    sim = Simulation(party.ALL)
    plot_coalitions(sim)

