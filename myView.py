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
    self.update_count = 0

  async def update_embed_task(self):
    self.working = True
    await asyncio.sleep(5)
    while self.working:
      self.update_count += 1
      embed = discord.Embed()
      embed.add_field(name='Counter', value=self.update_count)
      await self.message.edit(embed=embed)
      await asyncio.sleep(5)
  
  async def interaction_check(self, interaction: Interaction) -> bool:
    return interaction.user == self.user
  
  async def on_timeout(self) -> None:
    if self.message:
      await self.message.delete()
    return await super().on_timeout()
  
  @discord.ui.button(
    label='Cancel',
    row=0,
    style=discord.ButtonStyle.danger
  )
  async def cancel_button_callback(self, button, interaction: Interaction):
    button.disabled = True
    self.working = False
    await self.message.edit(view=self)
    await interaction.response.send_message('Goodbye!')
  
  @discord.ui.button(
    label='Work!',
    row=1,
    style=discord.ButtonStyle.primary,
    emoji='⚒️'
  )
  async def work_button_callback(self, button, interaction: Interaction):
    button.disabled = True
    embed = discord.Embed()
    embed.add_field(name='Counter', value=self.update_count)
    await interaction.response.edit_message(view=self, embed=embed)
    await self.update_embed_task()
