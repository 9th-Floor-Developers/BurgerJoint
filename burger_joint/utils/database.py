import json
import os
from pathlib import Path
from typing import Any

from burger_joint.model.player import Player


def json_path() -> str:
	base_dir = Path(__file__).resolve().parent.parent
	data_path = os.path.join(
		base_dir, 'assets', 'data.json'
	)
	return data_path


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
		file.append(player.__dict__)
		f.seek(0)
		json.dump(file, f, indent=4)
		f.truncate()
