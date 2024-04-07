import Prizepicks_API_Helper
import pandas as pd
from datetime import datetime, timedelta
import pytz
import os

api_url = "https://partner-api.prizepicks.com/projections?league_id=7&per_page=250&single_stat=true"
today_data = Prizepicks_API_Helper.data_collection(api_url)

desired_timezone = 'US/Pacific'
tz = pytz.timezone(desired_timezone)
current_date = datetime.now(tz)
added_date = current_date + timedelta(hours=2)
date = added_date.date()

prop_list = []
player_info_dict = {}

for player_entry in today_data['included']:
    player_id = player_entry['id']

    if player_entry['type'] == 'new_player':
        if '+' not in player_entry['attributes']['name']:
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
    if data_entry['attributes']['is_promo'] is False and data_entry['attributes']['odds_type'] == 'standard':
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
        game_id = data_entry['attributes']['game_id']
        start_time = data_entry['attributes']['start_time']

        prop_dict = {
            "Player_ID": player_id,
            'Name': player_name,
            'Position': player_position,
            'Team': team_name,
            'Opponent': opponent,
            'Line_Score': line_score,
            'Stat_Type': stat_type,
            'Game_ID': game_id,
            'Start_Time': start_time
        }
        prop_list.append(prop_dict)

new_df = pd.DataFrame(prop_list)
new_df['Player_ID'] = new_df['Player_ID'].astype(int)
new_df['Line_Score'] = new_df['Line_Score'].astype(float)
new_df.sort_values(['Start_Time', 'Game_ID', 'Team', 'Name', 'Stat_Type'], ascending=(True, True, True, True, True))
print(new_df.head())
print(new_df.columns)
print(new_df.shape)

# Joining the new data with the old data
csv_name = f"{date}_NBA_Odds"
folder_path = #put a path here 
file_name = f"{csv_name}.csv"
file_path = os.path.join(folder_path, file_name)
if os.path.exists(file_path):
    existing_df = pd.read_csv(file_path)
    print(existing_df.columns)
    merged_df = pd.merge(existing_df,new_df, on=['Player_ID', 'Name', 'Stat_Type', 'Position', 'Opponent', 'Team',
                                                 'Game_ID', 'Start_Time'], suffixes=('_existing', '_x'), how='outer')
    print(merged_df.columns)
    merged_df['Line_Score_existing'] = merged_df['Line_Score_x'].combine_first(merged_df['Line_Score_existing'])
    merged_df = merged_df.drop(['Line_Score_x'], axis=1)
    merged_df.rename(columns={'Line_Score_existing': 'Line_Score'})
    merged_df.sort_values(['Start_Time', 'Game_ID', 'Name','Stat_Type'], ascending=(True, True, True, True),
                          inplace=True)
    print(merged_df)
    merged_df.sort_values(['Start_Time', 'Game_ID', 'Team', 'Name', 'Stat_Type'], ascending=(True, True, True, True,
                                                                                             True), inplace=True)
    merged_df = merged_df.drop_duplicates(
        subset=['Player_ID', 'Name', 'Stat_Type', 'Position', 'Opponent', 'Team', 'Game_ID'])

    merged_df.to_csv(file_path, index=False)
    print(merged_df.shape)
else:
    new_df.to_csv(file_path, index=False)

