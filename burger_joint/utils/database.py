import json
import os
from burger_joint.model.player import Player

playersDataPath = os.path.join('game_data', 'players_data.json')


def load_players_data():
	with open(playersDataPath, 'r') as f:
		return [Player(**data) for data in json.load(f)]


def save_players_data(data : list[Player]):
	with open(playersDataPath, 'w') as f:
		json.dump([player.__dict__ for player in data], f, indent=4)


