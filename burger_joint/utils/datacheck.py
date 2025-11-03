from discord import Color, Interaction

from burger_joint.utils import embeds


async def is_positive_int(
	n: str,
	interaction: Interaction,
	include_zero: bool = False,
	var_name: str = 'inputted number'
) -> bool:
	if not n.isdigit():
		await interaction.respond(
			embed=embeds.simple_embed(
				description_text=f'The {var_name} has to be a positive, whole number',
				embed_color=Color.red()
			),
			ephemeral=True
		)
		return False
	
	n = int(n)
	
	min_value = 0 if include_zero else 1
	if n < min_value:
		await interaction.respond(
			embed=embeds.simple_embed(
				description_text=f'The {var_name} cannot be less than {min_value}.',
				embed_color=Color.red()
			),
			ephemeral=True
		)
		return False
	
	return True
