"""
Файл для банальных привет и пока
"""
from discord.ext import commands
from discord import app_commands


# Собственно основной класс
class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Привет
    @app_commands.command(name='hello', description='Говорит привет '
                                                    'пользователю')
    async def say_hello(self, ctx):
        await ctx.response.send_message(f'Привет, {ctx.user.mention}',
                                        ephemeral=True)

    # Пока
    @app_commands.command(name='goodbye',
                          description='Говорит пока пользователю')
    async def say_goodbye(self, ctx):
        await ctx.response.send_message(f'Пока, {ctx.user.mention}!',
                                        ephemeral=True)

    # ...
    @app_commands.command(name='dont_use', description='Не надо, оно того '
                                                       'не стоит')
    async def dont_use(self, ctx):
        await ctx.response.send_message(f'Я предупреждал.\n @everyone,'
                                        f'{ctx.user.mention} нравится данное '
                                        f'видео 🤗: https://cdn.discordapp.com/'
                                        f'attachments/864504259575545881/'
                                        f'1098688869546872922/'
                                        f'300_Black_men_for_only_2_'
                                        f'pounds.mp4 \nА еще данная фотокар'
                                        f'точка 😍: https://cdn.discordapp.com/'
                                        f'attachments/864504259575545881/'
                                        f'1098690420801802291/'
                                        f'ojaljm69lsp71.jpg')


# Добавление в бота
async def setup(bot):
    await bot.add_cog(Greetings(bot))
    print('Greetings loaded')


# Убирание из бота
async def teardown(bot):
    await bot.remove_cog(Greetings(bot))
    print('Greetings unloaded')
