# import the necessary libraries

import pandas as pd  # this is for data processing with dataframes
import numpy as np   # this is for various number things like the random choice and the zeros array
import time
from team_path_map import BracketMap    # this allows us to access the data in the other file


def weighted_choice(sequence,  weights):
    x = np.random.randint(0,1e8)
    weights = [weight*1e8 for weight in weights]

    weights_dict = {el: prob for (el, prob) in zip(sequence, weights)}

    place = 0
    for el, prob in weights_dict.items():

        place = place + prob

        if place > x:
            return el



# ******** Prep Data *****************

# Creates an instance of the class described in team_path_map, giving us access to all the map data.
path_data = BracketMap()

# load the data and take only the columns we need.
all_forecast_data = pd.read_csv('./fivethirtyeight_ncaa_forecasts.csv')
round_wins_all = all_forecast_data[['rd1_win', 'rd2_win', 'rd3_win', 'rd4_win', 'rd5_win', 'rd6_win', 'rd7_win']]
round_wins = round_wins_all[137: 200]
team_names = all_forecast_data['team_name'][137:200]
round_wins_named = round_wins.set_index(team_names)




# ******** Algorithm ****************

brackets = pd.DataFrame()
# loop that runs 10,000 iterations
for i in range(10):


    # loop that iterates through the empty games
    # create empty bracket
    bracket = list(np.zeros(63))
    print(bracket)
    full = False
    while not full:
        game = bracket.index(0) + 1 # because of zero indexing

        # makes list of all teams playing in game
        possible_teams = [team for team in path_data.map_dict if game in path_data.map_dict[team]]

        # Find the round
        one_team = possible_teams[0]                # pick a random team from the possible ones (the first one)
        that_map = path_data.map_dict[one_team]     # get the map of that team
        round = that_map.index(game) + 2            # all teams

        # the probabilites of each of the teams winning in this round
        probabilities = list(round_wins_named['rd{}_win'.format(round)][possible_teams])
        print('\nGame number = {g} \nProbabilities = {p} \nPossible Teams (length {l}) = {t}'.format(g=game, p=probabilities, t=possible_teams, l=len(possible_teams)))

        # choose winner of game
       # winner = np.random.choice(possible_teams, 2, p=probabilities)[0]
        winner = weighted_choice(possible_teams, probabilities)

        # fill in upstream games with this winner
        games = path_data.map_dict[winner]
        for gam in games:
            if bracket[gam-1] == 0:
                bracket[gam-1] = winner

        # decide whether or not the bracket is full
        if 0 not in bracket:
            full = True

    print(bracket)
    bracket_frame = pd.DataFrame([bracket])
    #print(bracket_frame)
    brackets = brackets.append(bracket_frame)
    print('')
    time.sleep(1)

print('done')
