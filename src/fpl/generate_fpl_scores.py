import pandas as pd 
import logging
from os import listdir

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def generate_and_save_all_fpl_scores(input_folder,output_folder,output_base_name):
    season_files = find_csv_filenames(input_folder)
    for season_data_file in season_files:
        season = str(season_data_file.split("_")[0])
        logger.info("Creating FPL Stats for {} season".format(season))
        output_path = str(output_folder + "/" + season + "_" + output_base_name)
        raw_stats_df = pd.read_csv(season_data_file)
        fpl_scores_df = generate_fpl_scores_for_season(raw_stats_df)
        final_df = combine_raw_stats_with_fpl_scores(raw_stats_df,fpl_scores_df)
        final_df.to_csv(output_path,index=False)
        logger.info("Season {} Complete".format(season))


def find_csv_filenames(path_to_dir,suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [x for x in filenames if x.endswith(suffix)]


def generate_fpl_scores_for_season(raw_stats_df):
    # TODO: Generate scores
    return

def combine_raw_stats_with_fpl_scores(raw_stats_df,fpl_scores_df):
    # TODO: Combine dfs  
    return

if __name__ == '__main__':
    input_folder = "C:/Users/joeco/Python/fantasy-football-strategy/data/fbref"
    output_folder = "C:/Users/joeco/Python/fantasy-football-strategy/data/fpl/input"
    output_base_name = "full_player_fpl_scores.csv"
    generate_and_save_all_fpl_scores(input_folder,output_folder,output_base_name)