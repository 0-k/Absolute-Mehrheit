import matplotlib.pyplot as plt
from src.party import Party
from src.simulation import Simulation


if __name__ == '__main__':
    '''**  Try again. Fail again. Fail better. **'''

    cdu = Party(name='CDU', percentage=0.35, uncertainty=0.02)
    spd = Party(name='SPD', percentage=0.15, uncertainty=0.02)
    gruene = Party(name='GRUENE', percentage=0.18, uncertainty=0.02)
    fdp = Party(name='FDP', percentage=0.06, uncertainty=0.01)
    linke = Party(name='LINKE', percentage=0.09, uncertainty=0.01)
    afd = Party(name='AFD', percentage=0.11, uncertainty=0.02)
    other = Party(name='OTHER', percentage=0.06, uncertainty=0.01)
    election_outcomes = [cdu, spd, gruene, fdp, linke, afd, other]

    simulation = Simulation(election_outcomes)
    black_green = simulation.evaluate_coalition()

    plt.hist(black_green, bins=20)
    plt.show()
