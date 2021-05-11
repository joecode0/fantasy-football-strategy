import pandas as pd 
import logging
from os import listdir

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def generate_and_save_all_fpl_scores(input_folder,output_folder,output_base_name):
    season_files = find_csv_filenames(input_folder)
    for season_data_file in season_files:
        season = str(season_data_file.split("_")[0])
        logger.info("Creating FPL Stats for {} season".format(season))
        output_path = str(output_folder + "/" + season + "_" + output_base_name)
        raw_stats_df = pd.read_csv(season_data_file)
        raw_stats_df["fpl_points"] = raw_stats_df.apply(generate_fpl_score,axis=1)
        final_df.to_csv(output_path,index=False)
        logger.info("Season {} Complete".format(season))

def find_csv_filenames(path_to_dir,suffix=".csv"):
    filenames = listdir(path_to_dir)
    return [x for x in filenames if x.endswith(suffix)]

def generate_fpl_score(row):
    pos = convert_pos(str(row["pos"]))
    total_points = 0 
    # Playing time points
    mins = int(row["mins"])
    if mins > 0:
        if mins > 60:
            total_points += 2 
        else:
            total_points += 1 

    # Goals points
    goals = int(row["goals"])
    if pos == "GK" or pos == "DEF":
        total_points += (6*goals)
    elif pos == "MID":
        total_points += (5*goals)
    else: # pos == "ATT"
        total_points += (4*goals)

    # Assists points 
    assists = int(row["assists"])
    total_points += (3*assists)

    # TODO: Clean Sheet Points

    # TODO: Saves Points 

    # TODO: Penalty Save Points

    # Penalty Miss Points
    pens_att = int(row["pens_att"])
    pens_made = int(row["pens_made"])
    pens_missed = pens_att - pens_made
    total_points -= (2*pens_missed)

    # TODO: Bonus Points

    # TODO: Goals Conceded Points 

    # Yellow Card Points 
    cards_yellow = int(row["cards_yellow"])
    total_points -= cards_yellow 

    # Red Card Points 
    cards_red = int(row["cards_red"])
    total_points -= (2*cards_red)

    # Own Goal Points 
    own_goals = int(row["own_goals"])
    total_points -= (3*own_goals)

    return total_points
    
def convert_pos(pos):
    pos = pos.split(",")[0].strip()
    if pos == "GK":
        return "GK"
    elif pos == "FW":
        return "ATT"
    elif pos == "RW" or pos == "LW" or pos == "AM" or pos == "DM" or pos == "CM" or pos == "LM" or pos == "RM":
        return "MID"
    elif pos == "LB" or pos == "CB" or pos == "RB" or pos == "WB":
        return "DEF"
    else:
        logging.error("Invalid Pos: {}".format(pos))
        sys.exit(0)

if __name__ == '__main__':
    input_folder = "C:/Users/joeco/Python/fantasy-football-strategy/data/fbref"
    output_folder = "C:/Users/joeco/Python/fantasy-football-strategy/data/fpl/input"
    output_base_name = "full_player_fpl_scores.csv"
    generate_and_save_all_fpl_scores(input_folder,output_folder,output_base_name)