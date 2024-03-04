from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog
import pandas as pd


def get_player_id(name):
    player_dict = players.get_players()
    player = [player for player in player_dict if player['full_name'].lower() == name.lower()]
    if player:
        return player[0]['id']
    else:
        raise ValueError(f"Player {name} not found")


def get_player_stats(name):
    player_id = get_player_id(name)
    game_log = playergamelog.PlayerGameLog(player_id=player_id, season="2020-21")
    dataframe = game_log.get_data_frames()[0]
    return dataframe


def prepare_features(df):
    expected_columns = ['PTS', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'REB', 'AST', 'STL', 'BLK', 'PF']
    missing_columns = [col for col in expected_columns if col not in df.columns]
    for col in missing_columns:
        df[col] = 0

    features = df[expected_columns].copy()
    print(features)
    return features


def get_matching_players(query):
    player_dict = players.get_players()
    matching_players = [player['full_name'] for player in player_dict if query.lower() in player['full_name'].lower()]
    return matching_players
