import discord
from discord import *
from monster import Monster
from player import Player

class myView(discord.ui.View):
  def __init__(
    self,
    *items,
    timeout: Optional[float] = 600,
    user,
    player: Player
  ):
    super().__init__(*items, timeout=timeout)
    self.user = user
    self.update_count = 0
    self.player: Player = player
    self.monster: None | Monster = None

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
    row=0,
    style=discord.ButtonStyle.primary,
    emoji='⚒️'
  )
  async def work_button_callback(self, button, interaction: Interaction):
    button.disabled = True
    embed = discord.Embed()
    embed.add_field(name='Counter', value=self.update_count)
    await interaction.response.edit_message(view=self, embed=embed)
    await self.update_embed_task()
  
  def spawn_monster(self):
    level = self.player.level
    match level:
      case 1:
        monster_name = 'Rat'
      case 2:
        monster_name = 'Boar'
      case _:
        monster_name = 'Goblin'
    
    self.monster = Monster(
      name=monster_name,
      level=level,
      health=level * 20,
      max_health=level * 20
    )

  def hunt_embed(self) -> Embed:
    embed = Embed(title='The Hunt Has Begun' ,color=Colour.dark_red())
    embed.set_image(url='https://www.fao.org/images/devforestslibraries/default-album/forests.jpg?sfvrsn=2dd96b96_11')

    #? + .5 added so that int acts as 'round' instead of 'floor'
    health_proportion = int((10 * self.player.health / self.player.max_health) + .5)
    embed.description = ('**Player Health**\n' + str(self.player.health) + ' '
                        + '🟩🟩🟩🟩🟩🟩🟩🟩🟩🟩'[:health_proportion]
                        + '⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜'[: 10 - health_proportion]
                        + ' ' + str(self.player.max_health))

    embed.add_field(name='Monsters Defeated', value=self.monsters_defeated)
    embed.add_field(name='Player Level', value=self.player.level)
    embed.add_field(name='Player Experience', value=self.player.experience)
    embed.add_field(name='Silver', value=self.player.silver)

    if self.monster:
      embed.title = f'A wild {self.monster.name.lower()} has appeared!'
      monster_health_proportion = int((10 * self.monster.health / self.monster.max_health) + .5)
      monster_health_bar = (str(self.monster.health) + ' '
                        + '🟥🟥🟥🟥🟥🟥🟥🟥🟥🟥'[:monster_health_proportion]
                        + '⬜⬜⬜⬜⬜⬜⬜⬜⬜⬜'[: 10 - monster_health_proportion]
                        + ' ' + str(self.monster.max_health))
      embed.add_field(
        name=f'{self.monster.name} health',
        value=monster_health_bar,
        inline=False
      )
      match self.monster.name:
        case 'Rat':
          embed.set_image(url = 'https://cdn.britannica.com/26/65326-050-53232216/Norway-rat.jpg?q=60')
        case 'Boar':
          embed.set_image(url = 'https://ichef.bbci.co.uk/news/976/cpsprodpb/C138/production/_105146494_2ca4093f-f1ed-4db6-b2c0-555d9676a95c.jpg')
        case 'Goblin':
          embed.set_image(url = 'https://kanto.legiaodosherois.com.br/w760-h398-cfill/wp-content/uploads/2021/12/legiao_bqoNvUSi5cEV.png.webp')
    else:
      embed.add_field(name="It's quiet for now", value="🏕️", inline=False)
    return embed

  @discord.ui.button(
    label='Start Hunting',
    row=1,
    style=discord.ButtonStyle.green,
    emoji='🏹'
  )
  async def start_hunting(self, button: Button, interaction: Interaction):
    self.disable_all_items()
    await interaction.response.edit_message(view=self)

    self.next_to_attack: 'Player' | 'Monster' = 'Player'
    self.monsters_defeated: int = 0

    while True:
      if not self.monster:
        self.spawn_monster()
        embed = self.hunt_embed()
        await interaction.message.edit(view=self, embed=embed)
        #? when the monster has just spawned, wait 1 cycle before attacking
        #? so it is shown with full life once before battle
        await asyncio.sleep(2)
        continue

      match self.next_to_attack:
        case 'Player':
          self.monster.health -= self.player.level * 5
          self.next_to_attack = 'Monster'
        case 'Monster':
          self.player.health -= self.monster.level * 2
          self.next_to_attack = 'Player'

      if self.player.health <= 0:
        await interaction.message.reply('You have died')
        self.enable_all_items()
        embed = self.hunt_embed()
        await interaction.message.edit(view=self, embed=embed)
        self.player.health = self.player.max_health
        break

      if self.monster.health <= 0:
        self.player.silver += self.monster.level * 5
        self.player.experience += 10
        self.monsters_defeated += 1
        #? new monster, player attacks first
        self.next_to_attack = 'Player'
        self.monster = None
      
      if self.player.experience >= 100:
        self.player.experience = 0
        self.player.level += 1
      
      if self.player.level >= 4:
        await interaction.message.reply('You won!')
        self.enable_all_items()
        button.disabled = True
        embed = self.hunt_embed()
        await interaction.message.edit(view=self, embed=embed)
        break

      embed = self.hunt_embed()

      await interaction.message.edit(embed=embed)

      await asyncio.sleep(2)
