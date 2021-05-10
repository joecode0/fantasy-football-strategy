import pandas as pd
# from proxy_requests import ProxyRequests
# import requests
# from bs4 import BeautifulSoup as soup

def get_all_match_data(page):
    match_data = get_general_match_data(page)
    
    relevant_data = page.findAll("div",{"id":"content"})
    home_data,home_id = get_team_data(relevant_data,"home")
    away_data,away_id = get_team_data(relevant_data,"away")
    
    # Each is a list of dictionaries, each dict is a row of df
    list_of_series = []
    for d in home_data:
        d["id"] = home_id
        series = pd.Series(d)
        list_of_series.append(series)
    for d in away_data:
        d["id"] = away_id
        series = pd.Series(d)
        list_of_series.append(series)
    df = pd.DataFrame(list_of_series)
    
    match_data_duplicated = {}
    for key in match_data.keys():
        item = match_data[key]
        match_data_duplicated[key] = [item]*len(df)
        
    df_match_data = pd.DataFrame(match_data_duplicated)
    
    df_final = pd.concat([df,df_match_data],axis=1)
    return df_final

def get_general_match_data(page):
    relevant_data = page.findAll("div",{"class":"scorebox"})[0]
    divs = relevant_data.findAll("div",recursive=False)
    home_data = divs[0]
    away_data = divs[1]
    generic_data = divs[2]
    d = {}
    
    d["home_name"] = str(home_data.find("a").text)
    d["home_score"] = int(home_data.find("div",{"class":"score"}).text)
    d["home_xg"] = float(home_data.find("div",{"class":"score_xg"}).text)
    d["home_manager"] = str(home_data.find("div",{"class":"datapoint"}).text.split(": ")[-1])

    d["away_name"] = str(away_data.find("a").text)
    d["away_score"] = int(away_data.find("div",{"class":"score"}).text)
    d["away_xg"] = float(away_data.find("div",{"class":"score_xg"}).text)
    d["away_manager"] = str(away_data.find("div",{"class":"datapoint"}).text.split(": ")[-1])
    
    d["date"] = str(generic_data.find("a").text)
    d["time"] = str(generic_data.find("span").text.split(" (")[0])
    d["matchweek"] = int(str(generic_data.findAll("div")[1].text.split(" (")[1].split(" ")[-1])[:-1])
    d["stadium"] = str(generic_data.findAll("small")[1].text)
    spans = generic_data.findAll("span",{"style":"display:inline-block"})
    d["ref"] = str(spans[0].text.split(" (")[0])
    d["var_ref"] = str(spans[-1].text.split(" (")[0])
    
    return d

def get_team_data(team_wrapper,side):
    all_tables = team_wrapper[0].findAll("div",{"class":"table_wrapper tabbed"})
    #print(all_tables[0])
    if side == "home":
        table = all_tables[0].find("div",{"class":"table_container current"})
    elif side == "away":
        table = all_tables[1].find("div",{"class":"table_container current"})
        
    team_id_original = str(table["id"])
    team_id = team_id_original.split("_")[2]
    if side == "home":
        table = all_tables[0]
    elif side == "away":
        table = all_tables[1]
    
    
    summary_html = table.find("div",{"id":"div_stats_" + team_id + "_summary"}).tbody
    summary = read_table_data(summary_html)
    
    passing_html = table.find("div",{"id":"div_stats_" + team_id + "_passing"}).tbody
    passing = read_table_data(passing_html)
    
    passing_types_html = table.find("div",{"id":"div_stats_" + team_id + "_passing_types"}).tbody
    passing_types = read_table_data(passing_types_html)
    
    defense_html = table.find("div",{"id":"div_stats_" + team_id + "_defense"}).tbody
    defense = read_table_data(defense_html)
    
    possession_html = table.find("div",{"id":"div_stats_" + team_id + "_possession"}).tbody
    possession = read_table_data(possession_html)
    
    misc_html = table.find("div",{"id":"div_stats_" + team_id + "_misc"}).tbody
    misc = read_table_data(misc_html)
    
    output = combine_team_data([summary,passing,passing_types,defense,possession,misc])
    return output,team_id
    
def read_table_data(table_html):
    all_player_data = []
    player_html_list = table_html.findAll("tr")
    for player_html in player_html_list:
        player_data = read_player_table_data(player_html)
        all_player_data.append(player_data)
    # all_player_data is a list of dicts, 1 dict per player of their summary data
    return all_player_data

def read_player_table_data(player_html):
    a = {}
    a["name"] = player_html.th.a.text
    inner_data = player_html.findAll("td")
    a["pos"] = inner_data[2].text
    a["age"] = inner_data[3].text.split("-")[0]
    for i in range(4,len(inner_data)):
        a[str(inner_data[i]["data-stat"])] = inner_data[i].text
    return a

def combine_team_data(datasets):
    data_by_player = {}
    # First create dict key for each player name
    for d in datasets[0]:
        data_by_player[d["name"]] = []
    # Go through each dataset and update data_by_player
    for dataset in datasets:
        # Go through each player data and add to data_by_player dict of lists
        for i in range(len(dataset)):
            player_dict = dataset[i]
            player_name = player_dict["name"]
            data_by_player[player_name] += [player_dict]
    
    # Now each entry in data_by_player is a list of dictionaries of data points
    output_list = []
    for key in data_by_player.keys():
        p = data_by_player[key]
        merged_data = {**p[0],**p[1],**p[2],**p[3],**p[4],**p[5]}
        output_list += [merged_data]
        
    return output_list