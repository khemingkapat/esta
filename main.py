from utils import *
import pandas as pd
import os

from utils.general import camel_to_snake

parsed = {
    "matches": list(),
    "rounds": list(),
    "kills": list(),
    "damages": list(),
    "grenades": list(),
    "bomb_events": list(),
    "weapon_fires": list(),
    "flashes": list(),
    "frames": list(),
    "players": list(),
    "team_frames": list(),
    "player_frames": list(),
    "inventory": list(),
    "bomb_location": list(),
    "projectiles": list(),
    "smokes": list(),
    "fires": list(),
}

dir_path = "./decompressed/"
for filename in os.listdir(dir_path)[:5]:
    filepath = os.path.join(dir_path, filename)
    if not os.path.isfile(filepath):
        continue
    print(f"getting data from {filepath}")

    data = json_to_dict(filepath)
    match_data = dict(get_top_level(data))
    parsed["matches"].append(match_data)

    if "gameRounds" in data and data["gameRounds"]:
        for round in data["gameRounds"]:
            round_data = dict(get_top_level(round))
            round_id = len(parsed["rounds"])
            parsed["rounds"].append(round_data)

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

            if "kills" in round and round["kills"]:
                for kill in round["kills"]:
                    kill_data = dict(get_top_level(kill))
                    kill_data["round_id"] = round_id
                    parsed["kills"].append(kill_data)

            if "damages" in round and round["damages"]:
                for damage in round["damages"]:
                    damage_data = dict(get_top_level(damage))
                    damage_data["round_id"] = round_id
                    parsed["damages"].append(damage_data)

            if "grenades" in round and round["grenades"]:
                for grenade in round["grenades"]:
                    grenade_data = dict(get_top_level(grenade))
                    grenade_data["round_id"] = round_id
                    parsed["grenades"].append(grenade_data)

            if "bombEvents" in round and round["bombEvents"]:
                for bomb_event in round["bombEvents"]:
                    bomb_event_data = dict(get_top_level(bomb_event))
                    bomb_event_data["round_id"] = round_id
                    parsed["bomb_events"].append(bomb_event_data)

            if "weaponFires" in round and round["weaponFires"]:
                for weapon_fire in round["weaponFires"]:
                    weapon_fire_data = dict(get_top_level(weapon_fire))
                    weapon_fire["round_id"] = round_id
                    parsed["weapon_fires"].append(weapon_fire_data)

            if "flashes" in round and round["flashes"]:
                for flash in round["flashes"]:
                    flash_data = dict(get_top_level(flash))
                    flash_data["round_id"] = round_id
                    parsed["flashes"].append(flash_data)

            if "frames" in round and round["frames"]:
                for frame in round["frames"]:
                    frame_id = len(parsed["frames"])
                    frame_data = dict(get_top_level(frame))
                    frame_data["round_id"] = round_id
                    parsed["frames"].append(frame_data)

                    if "bomb" in frame and frame["bomb"]:
                        bomb_location_data = dict(get_top_level(frame["bomb"]))
                        bomb_location_data["round_id"] = round_id
                        bomb_location_data["frame_id"] = frame_id
                        parsed["bomb_location"].append(bomb_location_data)

                    if "projectiles" in frame and frame["projectiles"]:
                        for projectile in frame["projectiles"]:
                            projectile_data = dict(get_top_level(projectile))
                            projectile_data["round_id"] = round_id
                            projectile_data["frame_id"] = frame_id
                            parsed["projectiles"].append(projectile_data)

                    if "smokes" in frame and frame["smokes"]:
                        for smoke in frame["smokes"]:
                            smoke_data = dict(get_top_level(smoke))
                            smoke_data["round_id"] = round_id
                            smoke_data["frame_id"] = frame_id
                            parsed["smokes"].append(smoke_data)

                    if "fires" in frame and frame["fires"]:
                        for fire in frame["fires"]:
                            fire_data = dict(get_top_level(fire))
                            fire_data["round_id"] = round_id
                            fire_data["frame_id"] = frame_id
                            parsed["fires"].append(fire_data)

                    if (
                        "t" in frame
                        and frame["t"]
                        and "players" in frame["t"]
                        and frame["t"]["players"]
                    ):
                        t_team_frame_data = dict(get_top_level(frame["t"]))
                        t_team_frame_data["round_id"] = round_id
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
                            player_frame_data["round_id"] = round_id
                            player_frame_data["frame_id"] = frame_id
                            player_frame_data["player_id"] = player_id
                            parsed["player_frames"].append(player_frame_data)

                            if "inventory" in player and player["inventory"]:
                                for inventory in player["inventory"]:
                                    inventory_data = dict(get_top_level(inventory))
                                    inventory_data["round_id"] = round_id
                                    inventory_data["frame_id"] = frame_id
                                    inventory_data["player_id"] = player_id
                                    parsed["inventory"].append(inventory_data)

                    if (
                        "ct" in frame
                        and frame["ct"]
                        and "players" in frame["ct"]
                        and frame["ct"]["players"]
                    ):
                        ct_team_frame_data = dict(get_top_level(frame["ct"]))
                        ct_team_frame_data["round_id"] = round_id
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
                            player_frame_data["round_id"] = round_id
                            player_frame_data["frame_id"] = frame_id
                            player_frame_data["player_id"] = player_id
                            parsed["player_frames"].append(player_frame_data)

                            if "inventory" in player and player["inventory"]:
                                for inventory in player["inventory"]:
                                    inventory_data = dict(get_top_level(inventory))
                                    inventory_data["round_id"] = round_id
                                    inventory_data["frame_id"] = frame_id
                                    inventory_data["player_id"] = player_id
                                    parsed["inventory"].append(inventory_data)


destination_path = "./parsed"
for key, value in parsed.items():
    df = pd.DataFrame(value)
    df.columns = [camel_to_snake(col) for col in df.columns]
    df.to_parquet(f"{destination_path}/{key}.parquet")
