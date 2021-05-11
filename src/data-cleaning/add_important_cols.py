import pandas as pd 
import logging
from os import listdir

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def add_and_save_important_cols(input_folder,output_folder,output_base_name):
    season_files = find_csv_filenames(input_folder)
    for season_data_file in season_files:
        season = str(season_data_file.split("_")[0])
        logger.info("Improving Player Data for {} Season".format(season))
        output_path = str(output_folder + "/" + season + "_" + output_base_name)
        raw_stats_df = pd.read_csv(season_data_file)
        raw_stats_df.reset_index(drop=True,inplace=True)
        # Match IDs
        match_ids = generate_match_ids(raw_stats_df)
        raw_stats_df["match_id"] = pd.Series(match_ids)
        raw_stats_df["side"] = raw_stats_df.apply(generate_side,axis=1)
        

def find_csv_filenames(path_to_dir,suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [x for x in filenames if x.endswith(suffix)]

def generate_match_ids(raw_stats_df):
    # Iterate through, separate out player stats per game, then set match_id = home_id + "_" + away_id 
    max_length = len(raw_stats_df)
    match_ids = []
    while len(match_ids) < max_length:
        current_i = len(match_ids)
        current_row = raw_stats_df.iloc[current_i]
        current_home_name = str(current_row["home_name"])
        current_away_name = str(current_row["away_name"])
        temp_home_name = current_home_name
        temp_away_name = current_away_name
        temp_i = current_i
        while temp_home_name == current_home_name and temp_away_name == current_away_name:
            temp_i += 1
            temp_row = raw_stats_df.iloc[temp_i]
            temp_home_name = str(temp_row["home_name"])
            temp_away_name = str(temp_row["away_name"])
        # Now we've moved onto next game, so row i=len(match_ids) to row i=temp_i-1 are 1 game
        game_data = raw_stats_df.iloc[current_i:temp_i]
        team_ids = set(game_data["id"].tolist())
        if len(team_ids) == 2:
            match_id = str(team_ids[0]) + "_" + str(team_ids[1])
        new_match_ids = [match_id]*(len(game_data))
        match_ids = match_ids + new_match_ids
    return match_ids

def generate_side(row):
    match_id = str(row["match_id"])
    team_id = str(row["id"])
    home_team = match_id.split("_")[0]
    if team_id == home_team:
        return "home"
    else:
        away_team = match_id.split("_")[1]
        if team_id == away_team:
            return "away"
        else:
            logger.error("Invalid ids: {}, {} & {}".format(match_id,home_team,away_team))
            sys.exit(0)

if __name__ == '__main__':
    input_folder = "C:/Users/joeco/Python/fantasy-football-strategy/data/fbref"
    output_folder = "C:/Users/joeco/Python/fantasy-football-strategy/data/fbref/cleaning"
    output_base_name = "improved_player_data.csv"
    add_and_save_important_cols(input_folder,output_folder,output_base_name)