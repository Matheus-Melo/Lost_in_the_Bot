from mimetypes import init


class Player():
    def __init__(
        self,
        discord_id: int,
        name: str,
        level: int,
        experience: int,
        silver: int,
        health: int,
        max_health: int
    ) -> None:
        self.discord_id = discord_id
        self.name = name
        self.level = level
        self.experience = experience
        self.silver = silver
        self.health = health
        self.max_health = max_health
