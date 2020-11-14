import matplotlib.pyplot as plt
from src.party import Party
from src.simulation import Simulation


if __name__ == '__main__':
    '''**  Try again. Fail again. Fail better. **'''

    union = Party(name='UNION', percentage=0.35, uncertainty=0.02, drift=0.03)
    spd = Party(name='SPD', percentage=0.15, uncertainty=0.02, drift=0.03)
    gruene = Party(name='GRUENE', percentage=0.18, uncertainty=0.02, drift=0.03)
    fdp = Party(name='FDP', percentage=0.06, uncertainty=0.01, drift=0.02)
    linke = Party(name='LINKE', percentage=0.09, uncertainty=0.01, drift=0.02)
    afd = Party(name='AFD', percentage=0.11, uncertainty=0.02, drift=0.02)
    other = Party(name='OTHER', percentage=0.06, uncertainty=0.01, drift=0.01)
    election_outcomes = [union, spd, gruene, fdp, linke, afd, other]

    simulation = Simulation(election_outcomes)

    black_green = [union, gruene]
    black_red = [union, spd]
    green_red_red = [gruene, spd, linke]
    black_yellow = [union, fdp]

    black_green_result = simulation.evaluate_coalition(black_green)
    black_red_result = simulation.evaluate_coalition(black_red)
    green_red_red_result = simulation.evaluate_coalition(green_red_red)
    black_yellow_result = simulation.evaluate_coalition(black_yellow)

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

