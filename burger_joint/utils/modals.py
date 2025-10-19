import discord 
from discord import ui

class SettingAddedMenuItemModal(ui.Modal, title='Adding item'):
    def __init__(self):
        super().__init__()



    async def on_submit(self, interaction: discord.Interaction):
        pass
        