class Monster():
    def __init__(
        self,
        name: str,
        level: int,
        health: int,
        max_health: int
    ) -> None:
        self.name = name
        self.level = level
        self.health = health
        self.max_health = max_health
