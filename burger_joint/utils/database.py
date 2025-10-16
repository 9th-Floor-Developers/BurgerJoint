import json
import os
from enum import Enum
from pathlib import Path
from typing import Any

from discord import User

from burger_joint.model.player import Player
from burger_joint.utils import BadgeID


def json_path() -> str:
	base_dir = Path(__file__).resolve().parent.parent
	data_path = os.path.join(
		base_dir, 'assets', 'data.json'
	)
	return data_path


def create_new_player(user: User):
	player = Player(
		user_id=user.id, username=user.name,
		shop_name=f"{user.name}'s Burger Joint", balance=100, level=1,
		xp=0, burgers_sold=0, upgrades=[], employees=[], badges=set(),
		prestige=0
	)
	save_data(player)
	return player


def get_player(id: int) -> Player | None:
	with open(json_path()) as f:
		file: list[dict[str, Any]] = json.load(f)
		
		for player_json in file:
			if player_json['user_id'] == id:
				player = Player(**player_json)  # sets badges as type list
				
				player.badges = {
					BadgeID(badge)
					for badge in player.badges
				}
				
				return player
	return None


def get_all_players() -> list[Player]:
	with open(json_path()) as f:
		file: list[dict[str, Any]] = json.load(f)
		players: list[Player] = []
		
		for player_json in file:
			players.append(Player(**player_json))
		
		return players


def json_convert(obj: Any):
	if isinstance(obj, Enum):
		return obj.value
	if isinstance(obj, set):
		return list(obj)
	if hasattr(obj, "__dict__"):
		return obj.__dict__
	return obj


def save_data(player: Player) -> None:
	with open(json_path(), 'r+') as f:
		non_user_data: list[dict[str, Any]] = json.load(f)
		
		non_user_data = [data for data in non_user_data if
			data['user_id'] != player.user_id]
		
		user_data = json.loads(
			json.dumps(player.__dict__, default=json_convert)
		)
		
		non_user_data.append(user_data)
		
		f.seek(0)
		json.dump(non_user_data, f, indent=4)
		f.truncate()
