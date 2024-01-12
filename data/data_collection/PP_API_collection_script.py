import Prizepicks_API_Helper
import pandas as pd
from datetime import date
import os

api_url = "https://partner-api.prizepicks.com/projections?league_id=7&per_page=250&single_stat=true"
today_data = Prizepicks_API_Helper.data_collection(api_url)

date = date.today()
prop_list = []
player_info_dict = {}

for player_entry in today_data['included']:
    player_id = player_entry['id']
    if player_entry['type'] == 'new_player':
        if not player_entry['attributes']['combo']:
            player_name = player_entry['attributes']['name']
            player_position = player_entry['attributes']['position']
            team_name = player_entry['attributes']['team']
            player_info_dict[player_id] = {
                'name': player_name,
                'position': player_position,
                'team': team_name
            }

for data_entry in today_data['data']:
    player_id = data_entry['relationships']['new_player']['data']['id']

    if player_info_dict.get(player_id, {}).get('name') is None:
        continue

    player_name = player_info_dict[player_id]['name']
    player_position = player_info_dict[player_id]['position']
    team_name = player_info_dict[player_id]['team']

    opponent = data_entry['attributes']['description']

    line_score_value = data_entry['attributes']['line_score']
    if isinstance(line_score_value, dict):
        if '$numberInt' in line_score_value:
            line_score = int(line_score_value['$numberInt'])
        elif '$numberDouble' in line_score_value:
            line_score = float(line_score_value['$numberDouble'])
        else:
            line_score = None
    else:
        line_score = line_score_value
    stat_type = data_entry['attributes']['stat_type']

    prop_dict = {
        "Player_ID": player_id,
        'Name': player_name,
        'Position': player_position,
        'Team': team_name,
        'Opponent': opponent,
        'Line_Score': line_score,
        'Stat_type': stat_type
    }
    prop_list.append(prop_dict)

new_df = pd.DataFrame(prop_list)
csv_name = f"{date}_NBA_Odds"
folder_path = "/Users/vivekgarg/PycharmProjects/pythonProject2" #will have to change this to get from the git repo files
file_name = f"{csv_name}.csv"
file_path = os.path.join(folder_path, file_name)
if os.path.exists(file_path):
    existing_df = pd.read_csv(file_path)
    merged_df = existing_df.merge(new_df, on=['player_id', 'name', 'line_type'], suffixes=('_existing', '_new'), how='left')

    new_df.to_csv(file_name,index=False)
