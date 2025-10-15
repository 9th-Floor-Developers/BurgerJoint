import os
import json

playersDataPath = 'game_data.json'


async def getPlayersData():
    with open(playersDataPath, 'r') as f:
        return json.load(f)
    
async def savePlayersData(data):
    with open(playersDataPath, 'w') as f:
        json.dump(data, f, indent=4)

async def addNewPlayer(user):
    data = await getPlayersData()
    if str(user.id) not in data:
        data[str(user.id)] = {
            'name': user.name,
            'id': user.id,
            'money': 0,
        }
        await savePlayersData(data)

async def getPlayer(user):
    data = await getPlayersData()
    return data.get(str(user.id), None)

