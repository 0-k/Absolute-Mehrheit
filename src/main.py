import matplotlib.pyplot as plt
from src.party import Party
from src.simulation import Simulation

union = Party(name='UNION', percentage=0.354, uncertainty=0.025, drift=0.02)
spd = Party(name='SPD', percentage=0.1538, uncertainty=0.019, drift=0.0163)
gruene = Party(name='GRUENE', percentage=0.1851, uncertainty=0.02, drift=0.0166)
fdp = Party(name='FDP', percentage=0.0638, uncertainty=0.01, drift=0.00897)
linke = Party(name='LINKE', percentage=0.0797, uncertainty=0.013, drift=0.00842)
afd = Party(name='AFD', percentage=0.102, uncertainty=0.016, drift=0.0156)
other = Party(name='OTHER', percentage=0.0612, uncertainty=0.01, drift=0.0098)
election_outcomes = [union, spd, gruene, fdp, linke, afd, other]


def plot_coalitions(simulation):
    black_green = [union, gruene]
    black_red = [union, spd]
    green_red_red = [gruene, spd, linke]
    black_yellow = [union, fdp]

    black_green_result = simulation.evaluate_seats_coalition(black_green)
    black_red_result = simulation.evaluate_seats_coalition(black_red)
    green_red_red_result = simulation.evaluate_seats_coalition(green_red_red)
    black_yellow_result = simulation.evaluate_seats_coalition(black_yellow)

    fig, axs = plt.subplots(2, 2)
    axs[0, 0].hist(black_green_result, bins=50, color='black')
    axs[0, 0].set_xlim(150, 450)
    axs[0, 0].set_title('Black Green')
    axs[0, 1].hist(black_red_result, bins=50, color='black')
    axs[0, 1].set_title('Black Red')
    axs[1, 0].hist(green_red_red_result, bins=50, color='black')
    axs[1, 0].set_title('Green Red Red')
    axs[1, 1].hist(black_yellow_result, bins=50, color='black')
    axs[1, 1].set_title('Black Yellow')

    axs[0, 0].set_xlim(150, 450)
    axs[0, 1].set_xlim(150, 450)
    axs[1, 0].set_xlim(150, 450)
    axs[1, 1].set_xlim(150, 450)

    axs[0, 0].axvline(300, color='red', linestyle='--')
    axs[0, 1].axvline(300, color='red', linestyle='--')
    axs[1, 0].axvline(300, color='red', linestyle='--')
    axs[1, 1].axvline(300, color='red', linestyle='--')
    plt.show()


def five_percent_hurdle(simulation, party):
    hurdle = simulation.evaluate_probability_hurdle_surpassing(party)
    print('Above 5 percent: ' + str(hurdle))

if __name__ == '__main__':
    '''**  Try again. Fail again. Fail better. **'''

    sim = Simulation(election_outcomes)
    five_percent_hurdle(sim, fdp)
    plot_coalitions(sim)

