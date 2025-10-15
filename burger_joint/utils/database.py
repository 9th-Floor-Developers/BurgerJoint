import json

playersDataPath = 'game_data.json'


async def get_player_data():
	with open(playersDataPath, 'r') as f:
		return json.load(f)


async def save_player_data(data):
	with open(playersDataPath, 'w') as f:
		json.dump(data, f, indent=4)


async def add_new_player(user):
	data = await get_player_data()
	if str(user.id) not in data:
		data[str(user.id)] = {
			'name': user.name,
			'id': user.id,
			'money': 0,
		}
		await save_player_data(data)


async def get_player(user):
	data = await get_player_data()
	return data.get(str(user.id), None)
