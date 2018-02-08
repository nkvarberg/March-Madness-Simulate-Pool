# import the necessary libraries

import pandas as pd  # this is for data processing with dataframes
import numpy as np   # this is for various number things like the random choice and the zeros array

from team_path_map import BracketMap    # this allows us to access the data in the other file


# ******** Prep Data *****************

# Creates an instance of the class described in team_path_map, giving us access to all the map data.
path_data = BracketMap()

# load the data and take only the columns we need.
all_forecast_data = pd.read_csv('./fivethirtyeight_ncaa_forecasts.csv')
round_wins_all = all_forecast_data[['rd1_win', 'rd2_win', 'rd3_win', 'rd4_win', 'rd5_win', 'rd6_win', 'rd7_win']]
round_wins = round_wins_all[68: 136]
team_names = all_forecast_data['team_name'][68:136]
round_wins_named = round_wins.set_index(team_names)


# create empty bracket
bracket = list(np.zeros(63))
full = False
# ******** Algorithm ****************

# loop that runs 10,000 iterations

# loop that iterates through the empty games
while not full:
    game = bracket.index(0) + 1 # because of zero indexing

    # makes list of all teams playing in game
    possible_teams = [team for team in path_data.map_dict if game in path_data.map_dict[team]]

    # Find the round
    one_team = possible_teams[0]
    that_map = path_data.map_dict[one_team]
    round = that_map.index(game) + 2

    # the probabilites of each of the teams winning in this round
    probabilities = list(round_wins_named['rd{}_win'.format(round)][possible_teams])


    # choose winner of championship
    winner = np.random.choice(possible_teams, 1, p=probabilities)[0]

    games = path_data.map_dict[winner]

    for game in games:
        if bracket[game-1] == 0:
            bracket[game-1] = winner

    if 0 not in bracket:
        full = True

    print(bracket)

print('done')





