import discord 
from discord import ui
#from burger_joint.model import MenuItem
#from burger_joint.utils import FoodItemID


class SettingAddedMenuItemModal(ui.Modal):
    def __init__(self, player, food_item_ID, food_item):
        super().__init__(title="Add Item to menu")
        self.player = player

        self.add_item(discord.ui.InputText(label="Name", value=food_item.name))
        self.add_item(discord.ui.InputText(label="Price", value=food_item.price))



    #async def on_submit(self, interaction: discord.Interaction):
    #    self.player.menu_items.append(MenuItem(
    #        food_item_ID=FoodItemID(self.food_item_ID.value),
    #        name=self.children[0].value,
    #        price=self.children[1].value,
    #        prestige=0
    #        ))
        

        