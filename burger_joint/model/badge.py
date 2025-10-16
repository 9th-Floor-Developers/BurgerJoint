from dataclasses import dataclass


@dataclass
class Badge:
	name: str
	icon: None  # some image format
	reward: int

# TODO Related Commands:
#  - /badges
