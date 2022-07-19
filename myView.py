import discord
from discord import *

class myView(discord.ui.View):
  def __init__(
    self,
    *items,
    timeout: Optional[float] = 180,
    user
  ):
    super().__init__(*items, timeout=timeout)
    self.user = user
  
  async def interaction_check(self, interaction: Interaction) -> bool:
    return interaction.user == self.user
  
  async def on_timeout(self) -> None:
    if self.message:
      await self.message.delete()
    return await super().on_timeout()
    