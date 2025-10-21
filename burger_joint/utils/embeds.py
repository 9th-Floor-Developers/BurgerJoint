"""Display various information as embeds."""

from discord import Color, Embed


def simple_embed(
	title_text: str = None,
	description_text: str = None,
	embed_color: Color = Color.green()
) -> Embed:
	return Embed(
		title=title_text,
		description=description_text,
		color=embed_color
	)
