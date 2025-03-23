import json
from utils import *
import pandas as pd

from utils.general import camel_to_snake


# import numpy as np

with open("./decompressed/example.json") as file:
    data = json.load(file)

parsed = {
    "games": list(),
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

for round in data["gameRounds"]:
    round_data = dict(get_top_level(round))
    round_id = len(parsed["rounds"])
    parsed["rounds"].append(round_data)

    for player in round["ctSide"]["players"]:
        player_data = dict(get_top_level(player))
        player_data["team_name"] = round["ctSide"]["teamName"]
        if player_data not in parsed["players"]:
            parsed["players"].append(player_data)

    for player in round["tSide"]["players"]:
        player_data = dict(get_top_level(player))
        player_data["team_name"] = round["tSide"]["teamName"]
        if player_data not in parsed["players"]:
            parsed["players"].append(player_data)

    for kill in round["kills"]:
        kill_data = dict(get_top_level(kill))
        kill_data["round_id"] = round_id
        parsed["kills"].append(kill_data)

    #
    for damage in round["damages"]:
        damage_data = dict(get_top_level(damage))
        damage_data["round_id"] = round_id
        parsed["damages"].append(damage_data)

    for grenade in round["grenades"]:
        grenade_data = dict(get_top_level(grenade))
        grenade_data["round_id"] = round_id
        parsed["grenades"].append(grenade_data)

    for bomb_event in round["bombEvents"]:
        bomb_event_data = dict(get_top_level(bomb_event))
        bomb_event_data["round_id"] = round_id
        parsed["bomb_events"].append(bomb_event_data)

    for weapon_fire in round["weaponFires"]:
        weapon_fire_data = dict(get_top_level(weapon_fire))
        weapon_fire["round_id"] = round_id
        parsed["weapon_fires"].append(weapon_fire_data)

    for flash in round["flashes"]:
        flash_data = dict(get_top_level(flash))
        flash_data["round_id"] = round_id
        parsed["flashes"].append(flash_data)

    for frame in round["frames"]:
        frame_id = len(parsed["frames"])
        frame_data = dict(get_top_level(frame))
        frame_data["round_id"] = round_id
        parsed["frames"].append(frame_data)

        bomb_location_data = dict(get_top_level(frame["bomb"]))
        bomb_location_data["round_id"] = round_id
        bomb_location_data["frame_id"] = frame_id
        parsed["bomb_location"].append(bomb_location_data)

        for projectile in frame["projectiles"]:
            projectile_data = dict(get_top_level(projectile))
            projectile_data["round_id"] = round_id
            projectile_data["frame_id"] = frame_id
            parsed["projectiles"].append(projectile_data)

        for smoke in frame["smokes"]:
            smoke_data = dict(get_top_level(smoke))
            smoke_data["round_id"] = round_id
            smoke_data["frame_id"] = frame_id
            parsed["smokes"].append(smoke_data)

        for fire in frame["fires"]:
            fire_data = dict(get_top_level(fire))
            fire_data["round_id"] = round_id
            fire_data["frame_id"] = frame_id
            parsed["fires"].append(fire_data)

        t_team_frame_data = dict(get_top_level(frame["t"]))
        t_team_frame_data["round_id"] = round_id
        t_team_frame_data["frame_id"] = frame_id
        parsed["team_frames"].append(t_team_frame_data)

        ct_team_frame_data = dict(get_top_level(frame["ct"]))
        ct_team_frame_data["round_id"] = round_id
        ct_team_frame_data["frame_id"] = frame_id
        parsed["team_frames"].append(ct_team_frame_data)

        for player in frame["t"]["players"]:
            player_frame_data = dict(get_top_level(player))
            player_id = parsed["players"].index(
                {
                    "playerName": player["name"],
                    "steamID": player["steamID"],
                    "team_name": t_team_frame_data["teamName"],
                }
            )
            player_frame_data["round_id"] = round_id
            player_frame_data["frame_id"] = frame_id
            player_frame_data["player_id"] = player_id
            parsed["player_frames"].append(player_frame_data)

            if player["inventory"] is None:
                pass
            else:
                for inventory in player["inventory"]:
                    inventory_data = dict(get_top_level(inventory))
                    inventory_data["round_id"] = round_id
                    inventory_data["frame_id"] = frame_id
                    inventory_data["player_id"] = player_id
                    parsed["inventory"].append(inventory_data)

        for player in frame["ct"]["players"]:
            player_frame_data = dict(get_top_level(player))
            player_id = parsed["players"].index(
                {
                    "playerName": player["name"],
                    "steamID": player["steamID"],
                    "team_name": ct_team_frame_data["teamName"],
                }
            )
            player_frame_data["round_id"] = round_id
            player_frame_data["frame_id"] = frame_id
            player_frame_data["player_id"] = player_id
            parsed["player_frames"].append(player_frame_data)

            if player["inventory"] is None:
                pass
            else:
                for inventory in player["inventory"]:
                    inventory_data = dict(get_top_level(inventory))
                    inventory_data["round_id"] = round_id
                    inventory_data["frame_id"] = frame_id
                    inventory_data["player_id"] = player_id
                    parsed["inventory"].append(inventory_data)


df = pd.DataFrame(parsed["fires"])
df.columns = [camel_to_snake(col) for col in df.columns]
df.to_csv("test.csv")
