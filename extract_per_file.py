from utils import *
import pandas as pd
import os
import gc

from utils.general import camel_to_snake

dir_path = "./decompressed/"
destination_path = "./parsed"

for filename in os.listdir(dir_path)[:100]:
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
                for frame in round["frames"]:
                    frame_id = len(parsed["frames"])
                    frame_data = dict(get_top_level(frame))
                    frame_data["round_num"] = round_num
                    parsed["frames"].append(frame_data)
                    del frame_data  # delete frame_data

                    if "bomb" in frame and frame["bomb"]:
                        bomb_location_data = dict(get_top_level(frame["bomb"]))
                        bomb_location_data["round_num"] = round_num
                        bomb_location_data["frame_id"] = frame_id
                        parsed["bomb_location"].append(bomb_location_data)
                        del bomb_location_data  # delete bomb_location_data

                    if "projectiles" in frame and frame["projectiles"]:
                        for projectile in frame["projectiles"]:
                            projectile_data = dict(get_top_level(projectile))
                            projectile_data["round_num"] = round_num
                            projectile_data["frame_id"] = frame_id
                            parsed["projectiles"].append(projectile_data)
                            del projectile_data  # delete projectile_data

                    if "smokes" in frame and frame["smokes"]:
                        for smoke in frame["smokes"]:
                            smoke_data = dict(get_top_level(smoke))
                            smoke_data["round_num"] = round_num
                            smoke_data["frame_id"] = frame_id
                            parsed["smokes"].append(smoke_data)
                            del smoke_data  # delete smoke_data

                    if "fires" in frame and frame["fires"]:
                        for fire in frame["fires"]:
                            fire_data = dict(get_top_level(fire))
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
                            player_frame_data["round_num"] = round_num
                            player_frame_data["frame_id"] = frame_id
                            player_frame_data["player_id"] = player_id
                            parsed["player_frames"].append(player_frame_data)
                            del player_frame_data  # delete player_frame_data
                            del player_data  # delete player_data
                            if "inventory" in player and player["inventory"]:
                                for inventory in player["inventory"]:
                                    inventory_data = dict(get_top_level(inventory))
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
                            player_frame_data["round_num"] = round_num
                            player_frame_data["frame_id"] = frame_id
                            player_frame_data["player_id"] = player_id
                            parsed["player_frames"].append(player_frame_data)
                            del player_frame_data  # delete player_frame_data
                            del player_data  # delete player_data
                            if "inventory" in player and player["inventory"]:
                                for inventory in player["inventory"]:
                                    inventory_data = dict(get_top_level(inventory))
                                    inventory_data["round_num"] = round_num
                                    inventory_data["frame_id"] = frame_id
                                    inventory_data["player_id"] = player_id
                                    parsed["inventory"].append(inventory_data)
                                    del inventory_data
                        del ct_team_frame_data

    for key, value in parsed.items():
        if value:  # check if list is not empty.
            df = pd.DataFrame(value)
            df.columns = [camel_to_snake(col) for col in df.columns]
            df.to_parquet(
                f"{destination_path}/{key}_{filename}.parquet"
            )  # add filename to parquet.
            del df
            gc.collect()
    del parsed
    del data
    gc.collect()
