import discord 
from discord import ui
from burger_joint.model import MenuItem, FoodItemID, Player, FoodItem, ALL_FOOD_ITEMS
from .database import save_data

class SettingAddedMenuItemModal(ui.Modal):
    def __init__(self, player: Player, food_item_ID: FoodItemID):
        super().__init__(title="Add Item to menu")
        self.player = player
        self.food_item_ID = food_item_ID
        self.food_item = ALL_FOOD_ITEMS[food_item_ID]

        self.add_item(discord.ui.InputText(label="Name", value=self.food_item.name))
        self.add_item(discord.ui.InputText(label="Price", value=self.food_item.price, style=discord.InputTextStyle.short))



    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Adding item to menu")
        embed.add_field(name="Name", value=self.children[0].value)
        embed.add_field(name="Price", value=self.children[1].value)
        await interaction.response.send_message(embeds=[embed])

        self.player.menu_items.append(MenuItem(
            food_item_ID=FoodItemID(self.food_item_ID.value),
            name=self.children[0].value,
            price=self.children[1].value,
            prestige=0
            ))
        save_data(self.player)
            
        

        