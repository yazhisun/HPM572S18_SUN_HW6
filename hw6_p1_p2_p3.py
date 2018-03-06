import numpy as np
import scr.StatisticalClasses as Stat


class Game(object):
    def __init__(self, id, prob_head):
        '''
        :param id: id of each flip
        :param prob_head:
        '''
        self._id = id
        self._rnd = np.random
        self._rnd.seed(id)
        self._probHead = prob_head  # probability of flipping a head
        self._countWins = 0  # number of wins, set to 0 to begin

    def simulate(self, n_of_flips):

        count_tails = 0  # number of consecutive tails so far, set to 0 to begin

        # flip the coin 20 times
        for i in range(n_of_flips):

            # in the case of flipping a heads
            if self._rnd.random_sample() < self._probHead:
                if count_tails >= 2:  # if the series is ..., T, T, H
                    self._countWins += 1  # increase the number of wins by 1
                count_tails = 0  # the tails counter needs to be reset to 0 because a heads was flipped

            # in the case of flipping a tails
            else:
                count_tails += 1  # increase tails count by one

    def get_reward(self):
        # calculate the reward from playing a single game
        return 100*self._countWins - 250


class SetOfGames:
    def __init__(self,prob_head,n_games):
        self._games = []
        self._gameRewards = [] # create an empty list where rewards will be stored
        self._n_games = n_games
        self._prob_h = prob_head
        self._loss = [] # create an enpty list to store

        # simulate the games
        for n in range(n_games):
            # create a new game
            game = Game(id=n, prob_head=self._prob_h)
            self._games.append(game)

    def simulate(self):
        for game in self._games:
            # simulate the game with 20 flips
            game.simulate(20)
            # store the reward
            self._gameRewards.append(game.get_reward())

        return GameOutcomes(self)

    def get_reward_list(self):
        """ returns all the rewards from all game to later be used for creation of histogram """
        return self._gameRewards

    def get_ave_reward(self):
        return sum(self._gameRewards)/len(self._gameRewards)

    def get_loss_list(self):
        for value in self._gameRewards:
            if value <0:
                self._loss.append(1)
            else:
                self._loss.append(0)
        return self._loss

    def get_probability_loss(self):
        """ returns the probability of a loss """

        return sum(self._loss)/len(self._loss)


class GameOutcomes:
    def __init__(self,simulated_set):
        self._simulated_set = simulated_set
        self._sumStat_rewards = \
            Stat.SummaryStat('The reward list of 1000 times is', self._simulated_set.get_reward_list())
        self._sumStat_prob_loss = \
            Stat.SummaryStat('The list of loss for 1000 times is',self._simulated_set.get_loss_list())

    def get_ave_reward(self):
        """ returns the average reward from all games"""
        return self._sumStat_rewards.get_mean()

    def get_CI_rewards(self, alpha):
        return self._sumStat_rewards.get_t_CI(alpha)

    def get_CI_prob_loss(self, alpha):
        return self._sumStat_prob_loss.get_t_CI(alpha)

    def get_PI_rewards(self, alpha):
        return self._sumStat_rewards.get_PI(alpha)


PROB_H = 0.5
NUM_OF_GAMES = 1000
ALPHA = 0.05

Trial = SetOfGames(prob_head = PROB_H, n_games = NUM_OF_GAMES)
gameOutcome = Trial.simulate()

# print(Trial.get_reward_list())
# print(Trial.get_loss_list())
# problem 1
print('The average expected reward is',Trial.get_ave_reward())
print('The 95% CI of average rewards', gameOutcome.get_CI_rewards(ALPHA))

print ('The probability of loosing a game is', Trial.get_probability_loss())
print('The 95% CI of probability of loss is', gameOutcome.get_CI_prob_loss(ALPHA))

# problem 2
# If we repeat this trial many times, 95% of trials will get an average rewards between -32.2 and -20.2
#If we repeat his trial many times, 95% of trials will have a probability of loosing game between 0.57 and 0.63

# problem 3
print('For the casino owner, the 95% confidence interval of average rewards is ', gameOutcome.get_CI_rewards(ALPHA))
print('For the gambler, the 95% prediction interval is',gameOutcome.get_PI_rewards(ALPHA))
# For the casino owner, he can play this game many times. There is 95% probability that his average reward will fall in this interval
# For the gambler, there is 95% probability that his next game will have reward in this prediction interval.



