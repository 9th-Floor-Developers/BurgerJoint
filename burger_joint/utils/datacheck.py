import discord
from discord import Color, ui, Embed
from utils import embeds

def represents_int(n : int) -> bool:
    try: 
        int(n)
    except ValueError:
        return False
    else:
        return True
    
async def is_positive_int(
        n : int,
        interaction : discord.Interaction,
        include_zero : bool = False,
        varible_name : bool = "inputed number"
        ) -> bool:
    if not represents_int(n):
        await interaction.respond(embed=embeds.simple_embed(
            description_text=f'The {varible_name} has to be a whole number',
			embed_color=Color.red()),
            ephemeral=True)
        return False
    n = int(n)
    if include_zero:
        if n < 0:
            await interaction.respond(embed=embeds.simple_embed(
                description_text=f'The {varible_name} cannot bet a negative number.',
                embed_color=Color.red()),
                ephemeral=True)
            return False
    else:
        if n < 1:
            await interaction.respond(embed=embeds.simple_embed(
                description_text=f'The {varible_name} cannot bet a negative number or zero.',
                embed_color=Color.red()),
                ephemeral=True)
            return False
    return True