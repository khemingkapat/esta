from .structure import *
from .general import *
import pandas as pd
import os
import gc


def downcast_df(df):
    for col, col_type in df.dtypes.items():
        str_type = str(col_type)
        if str_type.startswith("int"):
            df[col] = pd.to_numeric(df[col], downcast="integer")
        elif str_type.startswith("float"):
            df[col] = pd.to_numeric(df[col], downcast="float")
        elif col_type == "object" and df[col].nunique() <= (len(df) // 5):
            df[col] = df[col].astype("category")
    return df


def parse_by_join_file(
    dir_path="./decompressed", destination_path="./parsed/", total_matches=50
):
    for file_num, filename in enumerate(os.listdir(dir_path)[:total_matches]):
        filepath = os.path.join(dir_path, filename)
        if not os.path.isfile(filepath):
            continue
        print(f"getting data from {filepath}")

        data = json_to_dict(filepath)
        if data is None:
            continue

        parsed = {
            "matches": [],
            "rounds": [],
            "kills": [],
            "damages": [],
            "grenades": [],
            "bomb_events": [],
            "weapon_fires": [],
            "flashes": [],
            "frames": [],
            "players": [],
            # "player_rounds": [],
            "team_frames": [],
            "player_frames": [],
            "inventory": [],
            "bomb_location": [],
            "projectiles": [],
            "smokes": [],
            "fires": [],
        }

        match_data = dict(get_top_level(data))
        parsed["matches"].append(match_data)
        match_id = match_data["matchId"]
        del match_data

        if "gameRounds" in data and data["gameRounds"]:
            for round in data["gameRounds"]:
                round_data = dict(get_top_level(round))
                round_num = round_data["roundNum"]
                # print(round_num)
                round_data["match_id"] = match_id
                parsed["rounds"].append(round_data)
                del round_data  # delete round_data

                if (
                    "ctSide" in round
                    and round["ctSide"]
                    and "players" in round["ctSide"]
                    and round["ctSide"]["players"]
                ):
                    for player in round["ctSide"]["players"]:
                        ct_player_data = dict(get_top_level(player))
                        ct_player_data["team_name"] = round["ctSide"]["teamName"]
                        if ct_player_data not in parsed["players"]:
                            parsed["players"].append(ct_player_data)

                        # ct_player_round_data = ct_player_data.copy()
                        # ct_player_round_data["round_num"] = round_num
                        # ct_player_round_data["side"] = "ct"
                        # ct_player_round_data["match_id"] = match_id
                        # parsed["player_rounds"].append(ct_player_round_data)
                        del ct_player_data  # delete player_data

                if (
                    "tSide" in round
                    and round["tSide"]
                    and "players" in round["tSide"]
                    and round["tSide"]["players"]
                ):
                    for player in round["tSide"]["players"]:
                        t_player_data = dict(get_top_level(player))
                        t_player_data["team_name"] = round["tSide"]["teamName"]
                        if t_player_data not in parsed["players"]:
                            parsed["players"].append(t_player_data)

                        # t_player_round_data = t_player_data.copy()
                        # t_player_round_data["round_num"] = round_num
                        # t_player_round_data["side"] = "t"
                        # t_player_round_data["match_id"] = match_id
                        # parsed["player_rounds"].append(t_player_round_data)
                        del t_player_data  # delete player_data

                if "kills" in round and round["kills"]:
                    for kill in round["kills"]:
                        kill_data = dict(get_top_level(kill))
                        kill_data["round_num"] = round_num
                        kill_data["match_id"] = match_id
                        parsed["kills"].append(kill_data)
                        del kill_data  # delete kill_data

                if "damages" in round and round["damages"]:
                    for damage in round["damages"]:
                        damage_data = dict(get_top_level(damage))
                        damage_data["round_num"] = round_num
                        damage_data["match_id"] = match_id
                        parsed["damages"].append(damage_data)
                        del damage_data  # delete damage_data

                if "grenades" in round and round["grenades"]:
                    for grenade in round["grenades"]:
                        grenade_data = dict(get_top_level(grenade))
                        grenade_data["round_num"] = round_num
                        grenade_data["match_id"] = match_id
                        parsed["grenades"].append(grenade_data)
                        del grenade_data  # delete grenade_data

                if "bombEvents" in round and round["bombEvents"]:
                    for bomb_event in round["bombEvents"]:
                        bomb_event_data = dict(get_top_level(bomb_event))
                        bomb_event_data["round_num"] = round_num
                        bomb_event_data["match_id"] = match_id
                        parsed["bomb_events"].append(bomb_event_data)
                        del bomb_event_data  # delete bomb_event_data

                if "weaponFires" in round and round["weaponFires"]:
                    for weapon_fire in round["weaponFires"]:
                        weapon_fire_data = dict(get_top_level(weapon_fire))
                        weapon_fire_data["round_num"] = round_num
                        weapon_fire_data["match_id"] = match_id
                        parsed["weapon_fires"].append(weapon_fire_data)
                        del weapon_fire_data  # delete weapon_fire_data

                if "flashes" in round and round["flashes"]:
                    for flash in round["flashes"]:
                        flash_data = dict(get_top_level(flash))
                        flash_data["round_num"] = round_num
                        flash_data["match_id"] = match_id
                        parsed["flashes"].append(flash_data)
                        del flash_data  # delete flash_data

                if "frames" in round and round["frames"]:
                    for frame_id, frame in enumerate(round["frames"]):
                        frame_data = dict(get_top_level(frame))
                        frame_data["round_num"] = round_num
                        frame_data["match_id"] = match_id
                        parsed["frames"].append(frame_data)
                        del frame_data  # delete frame_data

                        if "bomb" in frame and frame["bomb"]:
                            bomb_location_data = dict(get_top_level(frame["bomb"]))
                            bomb_location_data["match_id"] = match_id
                            bomb_location_data["round_num"] = round_num
                            bomb_location_data["frame_id"] = frame_id
                            parsed["bomb_location"].append(bomb_location_data)
                            del bomb_location_data  # delete bomb_location_data

                        if "projectiles" in frame and frame["projectiles"]:
                            for projectile in frame["projectiles"]:
                                projectile_data = dict(get_top_level(projectile))
                                projectile_data["match_id"] = match_id
                                projectile_data["round_num"] = round_num
                                projectile_data["frame_id"] = frame_id
                                parsed["projectiles"].append(projectile_data)
                                del projectile_data  # delete projectile_data

                        if "smokes" in frame and frame["smokes"]:
                            for smoke in frame["smokes"]:
                                smoke_data = dict(get_top_level(smoke))
                                smoke_data["match_id"] = match_id
                                smoke_data["round_num"] = round_num
                                smoke_data["frame_id"] = frame_id
                                parsed["smokes"].append(smoke_data)
                                del smoke_data  # delete smoke_data

                        if "fires" in frame and frame["fires"]:
                            for fire in frame["fires"]:
                                fire_data = dict(get_top_level(fire))
                                fire_data["match_id"] = match_id
                                fire_data["round_num"] = round_num
                                fire_data["frame_id"] = frame_id
                                parsed["fires"].append(fire_data)
                                del fire_data  # delete fire_data

                        if (
                            "t" in frame
                            and frame["t"]
                            and "players" in frame["t"]
                            and frame["t"]["players"]
                        ):
                            t_team_frame_data = dict(get_top_level(frame["t"]))
                            t_team_frame_data["round_num"] = round_num
                            t_team_frame_data["match_id"] = match_id
                            t_team_frame_data["frame_id"] = frame_id
                            parsed["team_frames"].append(t_team_frame_data)

                            for player in frame["t"]["players"]:
                                player_frame_data = dict(get_top_level(player))
                                # if "inventory" in player_frame_data:
                                #     print(type(player_frame_data["inventory"]))
                                t_player_data = {
                                    "playerName": player["name"],
                                    "steamID": player["steamID"],
                                    "team_name": t_team_frame_data["teamName"],
                                }
                                if t_player_data not in parsed["players"]:
                                    parsed["players"].append(t_player_data)

                                # t_player_round_data = t_player_data.copy()
                                # t_player_round_data["round_num"] = round_num
                                # t_player_round_data["side"] = "t"
                                # t_player_round_data["match_id"] = match_id
                                # if t_player_round_data not in parsed["player_rounds"]:
                                #     parsed["player_rounds"].append(t_player_round_data)
                                #
                                # del t_player_round_data

                                # player_id = parsed["players"].index(t_player_data)
                                player_frame_data["match_id"] = match_id
                                player_frame_data["round_num"] = round_num
                                player_frame_data["frame_id"] = frame_id
                                # player_frame_data["player_id"] = player_id
                                parsed["player_frames"].append(player_frame_data)
                                del player_frame_data  # delete player_frame_data
                                del t_player_data  # delete player_data
                                if "inventory" in player and player["inventory"]:
                                    for inventory in player["inventory"]:
                                        inventory_data = dict(get_top_level(inventory))
                                        inventory_data["match_id"] = match_id
                                        inventory_data["round_num"] = round_num
                                        inventory_data["frame_id"] = frame_id
                                        inventory_data["player_id"] = player["steamID"]
                                        parsed["inventory"].append(inventory_data)
                                        del inventory_data
                            del t_team_frame_data

                        if (
                            "ct" in frame
                            and frame["ct"]
                            and "players" in frame["ct"]
                            and frame["ct"]["players"]
                        ):
                            ct_team_frame_data = dict(get_top_level(frame["ct"]))
                            ct_team_frame_data["round_num"] = round_num
                            ct_team_frame_data["match_id"] = match_id
                            ct_team_frame_data["frame_id"] = frame_id
                            parsed["team_frames"].append(ct_team_frame_data)

                            for player in frame["ct"]["players"]:
                                player_frame_data = dict(get_top_level(player))
                                ct_player_data = {
                                    "playerName": player["name"],
                                    "steamID": player["steamID"],
                                    "team_name": ct_team_frame_data["teamName"],
                                }
                                if ct_player_data not in parsed["players"]:
                                    parsed["players"].append(ct_player_data)

                                # ct_player_round_data = ct_player_data.copy()
                                # ct_player_round_data["round_num"] = round_num
                                # ct_player_round_data["side"] = "t"
                                # ct_player_round_data["match_id"] = match_id
                                # if ct_player_round_data not in parsed["player_rounds"]:
                                #     parsed["player_rounds"].append(ct_player_round_data)

                                # del ct_player_round_data

                                # player_id = parsed["players"].index(ct_player_data)
                                player_frame_data["match_id"] = match_id
                                player_frame_data["round_num"] = round_num
                                player_frame_data["frame_id"] = frame_id
                                # player_frame_data["player_id"] = player_id
                                parsed["player_frames"].append(player_frame_data)
                                del player_frame_data  # delete player_frame_data
                                del ct_player_data  # delete player_data
                                if "inventory" in player and player["inventory"]:
                                    for inventory in player["inventory"]:
                                        inventory_data = dict(get_top_level(inventory))
                                        inventory_data["match_id"] = match_id
                                        inventory_data["round_num"] = round_num
                                        inventory_data["frame_id"] = frame_id
                                        inventory_data["player_id"] = player["steamID"]
                                        parsed["inventory"].append(inventory_data)
                                        del inventory_data
                            del ct_team_frame_data

        for key, value in parsed.items():
            if value:
                df = pd.DataFrame(value).drop_duplicates()
                df.columns = [camel_to_snake(col) for col in df.columns]
                downcast_df(df)
                dest_file_name = f"{destination_path}/{key}.parquet"
                if not os.path.isfile(dest_file_name):
                    df.to_parquet(dest_file_name)
                else:
                    # print(f"found : {dest_file_name}")
                    exist_df = pd.read_parquet(dest_file_name)
                    joined_df = pd.concat([exist_df, df]).drop_duplicates()
                    downcast_df(joined_df)
                    joined_df.to_parquet(dest_file_name)
                    del exist_df
                    del joined_df
                del df
                gc.collect()

                print(f"saved {dest_file_name}, {file_num=}")
        del parsed
        del data
        gc.collect()


def parse_per_file(
    dir_path="./decompressed", destination_path="./parsed/", total_matches=50
):
    for file_num, filename in enumerate(os.listdir(dir_path)[:total_matches]):
        filepath = os.path.join(dir_path, filename)
        if not os.path.isfile(filepath):
            continue
        print(f"getting data from {filepath}")

        data = json_to_dict(filepath)
        if data is None:
            continue

        parsed = {
            "matches": [],
            "rounds": [],
            "kills": [],
            "damages": [],
            "grenades": [],
            "bomb_events": [],
            "weapon_fires": [],
            "flashes": [],
            "frames": [],
            "players": [],
            "player_rounds": [],
            "team_frames": [],
            "player_frames": [],
            "inventory": [],
            "bomb_location": [],
            "projectiles": [],
            "smokes": [],
            "fires": [],
        }

        match_data = dict(get_top_level(data))
        parsed["matches"].append(match_data)
        match_id = match_data["matchId"]
        del match_data

        if "gameRounds" in data and data["gameRounds"]:
            for round in data["gameRounds"]:
                round_data = dict(get_top_level(round))
                round_num = round_data["roundNum"]
                round_data["match_id"] = match_id
                parsed["rounds"].append(round_data)
                del round_data  # delete round_data

                if (
                    "ctSide" in round
                    and round["ctSide"]
                    and "players" in round["ctSide"]
                    and round["ctSide"]["players"]
                ):
                    for player in round["ctSide"]["players"]:
                        player_data = dict(get_top_level(player))
                        player_data["team_name"] = round["ctSide"]["teamName"]
                        if player_data not in parsed["players"]:
                            parsed["players"].append(player_data)
                        player_data["round_num"] = round_num
                        player_data["side"] = "ct"
                        player_data["match_id"] = match_id
                        parsed["player_rounds"].append(player_data)
                        del player_data  # delete player_data

                if (
                    "tSide" in round
                    and round["tSide"]
                    and "players" in round["tSide"]
                    and round["tSide"]["players"]
                ):
                    for player in round["tSide"]["players"]:
                        player_data = dict(get_top_level(player))
                        player_data["team_name"] = round["tSide"]["teamName"]
                        if player_data not in parsed["players"]:
                            parsed["players"].append(player_data)
                        player_data["round_num"] = round_num
                        player_data["side"] = "t"
                        player_data["match_id"] = match_id
                        parsed["player_rounds"].append(player_data)
                        del player_data  # delete player_data

                if "kills" in round and round["kills"]:
                    for kill in round["kills"]:
                        kill_data = dict(get_top_level(kill))
                        kill_data["round_num"] = round_num
                        kill_data["match_id"] = match_id
                        parsed["kills"].append(kill_data)
                        del kill_data  # delete kill_data

                if "damages" in round and round["damages"]:
                    for damage in round["damages"]:
                        damage_data = dict(get_top_level(damage))
                        damage_data["round_num"] = round_num
                        damage_data["match_id"] = match_id
                        parsed["damages"].append(damage_data)
                        del damage_data  # delete damage_data

                if "grenades" in round and round["grenades"]:
                    for grenade in round["grenades"]:
                        grenade_data = dict(get_top_level(grenade))
                        grenade_data["round_num"] = round_num
                        grenade_data["match_id"] = match_id
                        parsed["grenades"].append(grenade_data)
                        del grenade_data  # delete grenade_data

                if "bombEvents" in round and round["bombEvents"]:
                    for bomb_event in round["bombEvents"]:
                        bomb_event_data = dict(get_top_level(bomb_event))
                        bomb_event_data["round_num"] = round_num
                        bomb_event_data["match_id"] = match_id
                        parsed["bomb_events"].append(bomb_event_data)
                        del bomb_event_data  # delete bomb_event_data

                if "weaponFires" in round and round["weaponFires"]:
                    for weapon_fire in round["weaponFires"]:
                        weapon_fire_data = dict(get_top_level(weapon_fire))
                        weapon_fire_data["round_num"] = round_num
                        weapon_fire_data["match_id"] = match_id
                        parsed["weapon_fires"].append(weapon_fire_data)
                        del weapon_fire_data  # delete weapon_fire_data

                if "flashes" in round and round["flashes"]:
                    for flash in round["flashes"]:
                        flash_data = dict(get_top_level(flash))
                        flash_data["round_num"] = round_num
                        flash_data["match_id"] = match_id
                        parsed["flashes"].append(flash_data)
                        del flash_data  # delete flash_data

                if "frames" in round and round["frames"]:
                    for frame_id, frame in enumerate(round["frames"]):
                        frame_data = dict(get_top_level(frame))
                        frame_data["round_num"] = round_num
                        parsed["frames"].append(frame_data)
                        del frame_data  # delete frame_data

                        if "bomb" in frame and frame["bomb"]:
                            bomb_location_data = dict(get_top_level(frame["bomb"]))
                            bomb_location_data["match_id"] = match_id
                            bomb_location_data["round_num"] = round_num
                            bomb_location_data["frame_id"] = frame_id
                            parsed["bomb_location"].append(bomb_location_data)
                            del bomb_location_data  # delete bomb_location_data

                        if "projectiles" in frame and frame["projectiles"]:
                            for projectile in frame["projectiles"]:
                                projectile_data = dict(get_top_level(projectile))
                                projectile_data["match_id"] = match_id
                                projectile_data["round_num"] = round_num
                                projectile_data["frame_id"] = frame_id
                                parsed["projectiles"].append(projectile_data)
                                del projectile_data  # delete projectile_data

                        if "smokes" in frame and frame["smokes"]:
                            for smoke in frame["smokes"]:
                                smoke_data = dict(get_top_level(smoke))
                                smoke_data["match_id"] = match_id
                                smoke_data["round_num"] = round_num
                                smoke_data["frame_id"] = frame_id
                                parsed["smokes"].append(smoke_data)
                                del smoke_data  # delete smoke_data

                        if "fires" in frame and frame["fires"]:
                            for fire in frame["fires"]:
                                fire_data = dict(get_top_level(fire))
                                fire_data["match_id"] = match_id
                                fire_data["round_num"] = round_num
                                fire_data["frame_id"] = frame_id
                                parsed["fires"].append(fire_data)
                                del fire_data  # delete fire_data

                        if (
                            "t" in frame
                            and frame["t"]
                            and "players" in frame["t"]
                            and frame["t"]["players"]
                        ):
                            t_team_frame_data = dict(get_top_level(frame["t"]))
                            t_team_frame_data["round_num"] = round_num
                            t_team_frame_data["frame_id"] = frame_id
                            parsed["team_frames"].append(t_team_frame_data)

                            for player in frame["t"]["players"]:
                                player_frame_data = dict(get_top_level(player))
                                player_data = {
                                    "playerName": player["name"],
                                    "steamID": player["steamID"],
                                    "team_name": t_team_frame_data["teamName"],
                                }
                                if player_data not in parsed["players"]:
                                    parsed["players"].append(player_data)

                                player_id = parsed["players"].index(player_data)
                                player_frame_data["match_id"] = match_id
                                player_frame_data["round_num"] = round_num
                                player_frame_data["frame_id"] = frame_id
                                player_frame_data["player_id"] = player_id
                                parsed["player_frames"].append(player_frame_data)
                                del player_frame_data  # delete player_frame_data
                                del player_data  # delete player_data
                                if "inventory" in player and player["inventory"]:
                                    for inventory in player["inventory"]:
                                        inventory_data = dict(get_top_level(inventory))
                                        inventory_data["match_id"] = match_id
                                        inventory_data["round_num"] = round_num
                                        inventory_data["frame_id"] = frame_id
                                        inventory_data["player_id"] = player_id
                                        parsed["inventory"].append(inventory_data)
                                        del inventory_data
                            del t_team_frame_data

                        if (
                            "ct" in frame
                            and frame["ct"]
                            and "players" in frame["ct"]
                            and frame["ct"]["players"]
                        ):
                            ct_team_frame_data = dict(get_top_level(frame["ct"]))
                            ct_team_frame_data["round_num"] = round_num
                            ct_team_frame_data["frame_id"] = frame_id
                            parsed["team_frames"].append(ct_team_frame_data)

                            for player in frame["ct"]["players"]:
                                player_frame_data = dict(get_top_level(player))
                                player_data = {
                                    "playerName": player["name"],
                                    "steamID": player["steamID"],
                                    "team_name": ct_team_frame_data["teamName"],
                                }
                                if player_data not in parsed["players"]:
                                    parsed["players"].append(player_data)

                                player_id = parsed["players"].index(player_data)
                                player_frame_data["match_id"] = match_id
                                player_frame_data["round_num"] = round_num
                                player_frame_data["frame_id"] = frame_id
                                player_frame_data["player_id"] = player_id
                                parsed["player_frames"].append(player_frame_data)
                                del player_frame_data  # delete player_frame_data
                                del player_data  # delete player_data
                                if "inventory" in player and player["inventory"]:
                                    for inventory in player["inventory"]:
                                        inventory_data = dict(get_top_level(inventory))
                                        inventory_data["match_id"] = match_id
                                        inventory_data["round_num"] = round_num
                                        inventory_data["frame_id"] = frame_id
                                        inventory_data["player_id"] = player_id
                                        parsed["inventory"].append(inventory_data)
                                        del inventory_data
                            del ct_team_frame_data

        os.makedirs(f"{destination_path}/{match_id}", exist_ok=True)
        for key, value in parsed.items():
            if value:  # check if list is not empty.
                dest_file_name = f"{destination_path}/{match_id}/{key}_{filename.removesuffix('.json')}"
                df = pd.DataFrame(value)
                df.columns = [camel_to_snake(col) for col in df.columns]
                df.to_parquet(dest_file_name)  # add filename to parquet.
                print(f"saved {dest_file_name}")
                del df
                gc.collect()

        print(f"saved {destination_path}, {file_num=}")
        del parsed
        del data
        gc.collect()
