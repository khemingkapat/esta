from utils import *
import pandas as pd


# parse_by_join_file create single table for each object as seen in ./parsed/
# parse_by_join_file(
#     dir_path="./decompressed", destination_path="./parsed", total_matches=50
# )

# parse_per_file create subfolder for each every match named after match_id
# parse_per_file(
#     dir_path="./decompressed", destination_path="./parsed", total_matches=50
# )


file = lambda filename: f"./parsed/{filename}.parquet"
player_frames_df = pd.read_parquet(file("player_frames"))
players_df = pd.read_parquet(file("players"))
invetories_df = pd.read_parquet(file("inventory"))

players_steam_id = set(players_df.steam_id.unique())
player_frames_steam_id = set(player_frames_df.steam_id.unique())

print(players_steam_id == player_frames_steam_id)

print(invetories_df.info())
