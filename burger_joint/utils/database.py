import json
from model import Player 

playersDataPath = 'game_data.json'


async def load_player_data():
	with open(playersDataPath, 'r') as f:
		return json.load(f)


async def save_player_data(data : list[Player]):
	with open(playersDataPath, 'w') as f:
		json.dump(data, f, indent=4)

