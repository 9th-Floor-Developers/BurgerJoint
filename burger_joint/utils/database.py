import json
import os
from pathlib import Path
from typing import Any

from discord import User

from burger_joint.model.player import Player


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
		xp=0, burgers_sold=0, upgrades=[], employees=[], badges=[],
		prestige=0
	)
	save_data(player)
	return player

def get_player(id: int) -> Player | None:
	with open(json_path()) as f:
		file: list[dict[str, Any]] = json.load(f)
		for player_json in file:
			if player_json['user_id'] == id:
				return Player(**player_json)
	return None


def save_data(player: Player) -> None:
	with open(json_path(), 'r+') as f:
		file: list[dict[str, Any]] = json.load(f)
		
		for data in file:
			if data['user_id'] == player.user_id:
				file.remove(data)
				break
		
		file.append(player.__dict__)
		f.seek(0)
		json.dump(file, f, indent=4)
		f.truncate()
