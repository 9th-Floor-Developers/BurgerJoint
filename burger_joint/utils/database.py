import json
import os
from pathlib import Path

from burger_joint.model.player import Player


def json_path() -> str:
	base_dir = Path(__file__).resolve().parent.parent
	data_path = os.path.join(
		base_dir, 'assets', 'data.json'
	)
	return data_path


# TODO: update somehow with individual player data save/load
#  instead of reading/writing ALL player data
def load_players_data():
	with open(json_path(), 'r') as f:
		return [Player(**data) for data in json.load(f)]


def save_players_data(data: list[Player]):
	with open(json_path(), 'w') as f:
		json.dump([player.__dict__ for player in data], f, indent=4)
