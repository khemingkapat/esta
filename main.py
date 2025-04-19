from utils import *
import pandas as pd


# parse_by_join_file create single table for each object as seen in ./parsed/
parse_by_join_file(
    dir_path="./decompressed", destination_path="./parsed", total_matches=50
)

# parse_per_file create subfolder for each every match named after match_id
# parse_per_file(
#     dir_path="./decompressed", destination_path="./parsed", total_matches=50
# )

# player_rounds_df = pd.read_parquet("./parsed/player_rounds.parquet")
# print(player_rounds_df.drop_duplicates().shape)
# rounds_df = pd.read_parquet("./parsed/rounds.parquet")
# print(rounds_df.drop_duplicates().shape)


frames_df = pd.read_parquet("./parsed/frames.parquet")
print(frames_df)

player_frames_df = pd.read_parquet("./parsed/player_frames.parquet")
print(player_frames_df)
