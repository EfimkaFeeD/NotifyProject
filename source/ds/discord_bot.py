"""
Основной файл из которого запускается бот
"""
import discord
import cogs.utils.settings as settings
from cogs.utils.secret.discord_keys import BOT_KEY, DEV, GUILD
from discord.ext import commands

# Создание логирования
logger = settings.logging.getLogger('bot')


# Запуск бота
def run():
    # Префикс нужен для команд разработчика
    bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

    # При каждом запуске бота
    @bot.event
    async def on_ready():
        logger.info(f'User: {bot.user}')
        logger.info(f'Guild ID: {bot.guilds[0].id}')

        # Автоматическая загрузка файлов с набором команд
        for file in settings.COGS_DIR.glob('*.py'):
            if file != '__init__.py':
                await bot.load_extension(f'cogs.{file.name[:-3]}')

    # При добавлении на сервер
    @bot.event
    async def on_guild_join(guild):
        if guild.text_channels:
            await guild.text_channels[0].send('Привет, я погодный бот. '
                                              'Напишите "/help" чтобы узнать '
                                              'больше')

    # Команда доступная только разработчику для синхронизации с API Discord
    @bot.command(name='sync', hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def sync_commands(ctx):
        if str(ctx.guild.id) == GUILD and str(ctx.author.id) == DEV:
            try:
                await bot.tree.sync()
                logger.info('Successful syncing')
            except Exception as error:
                logger.info(f'While syncing error occurred: {error}')

    # Команда доступная только разработчику для остановки бота
    @bot.command(name='full_bot_stop', hidden=True)
    @commands.is_owner()
    @commands.guild_only()
    async def full_bot_stop(ctx):
        if str(ctx.guild.id) == GUILD and str(ctx.author.id) == DEV:
            try:
                for file in settings.COGS_DIR.glob('*.py'):
                    if file != '__init__.py':
                        await bot.unload_extension(f'cogs.{file.name[:-3]}')
            except Exception as error:
                logger.info(f'While unloading error occurred: {error}')
            await bot.close()

    # Перезагрузка отдельного файла команд
    @bot.tree.command(name='reload', description='Reloads specified cog')
    @commands.is_owner()
    async def reload_cogs(cog: str):
        await bot.reload_extension(f'cogs.{cog.lower()}')
        logger.info(f'Cog {cog} has been restarted')

    # Загрузка отдельного файла команд
    @bot.tree.command(name='load', description='Loads specified cog')
    @commands.is_owner()
    async def load_cogs(cog: str):
        await bot.load_extension(f'cogs.{cog.lower()}')
        logger.info(f'Cog {cog} has been loaded')

    # Выгрузка отдельного файла команд
    @bot.tree.command(name='unload', description='Unloads specified cog')
    @commands.is_owner()
    async def unload_cogs(cog: str):
        await bot.unload_extension(f'cogs.{cog.lower()}')
        logger.info(f'Cog {cog} has been unloaded')

    # Меню помощи (команда доступна всем пользователям)
    @bot.tree.command(name='help', description='Открывает меню с командами')
    async def help_menu(ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_embed(),
            title='Помощь',
            description="""
            Команды для погодного бота
            /help - вызов этого меню
            /hello - бот скажет вам привет
            /goodbye - бот скажет вам пока
            /dont_use - название говорит само за себя
            /weather [city] - выведет текущую погоду в городе [city] по \
            информации OpenWeatherAPI
            /weather [city] [hour] - выведет погоду в городе [city] на время \
            (текущее время + 3 часа * [hour]) по информации OpenWeatherAPI, \
            [hour] может быть от 1 до 40 включительно
            P.S. [city] может быть как на русском, так и на английском
            Есть еще команды для владельца, но вам о них не надо знать :D
            """
        )
        embed.set_thumbnail(url='https://media.discordapp.net/attachments/'
                                '864504259575545881/1102198867241468024/'
                                'bot_pic.jpg')
        embed.set_footer(text='Created by Efimka_FeeD#9598 with ❤️')
        await ctx.response.send_message(embed=embed, ephemeral=True)

    # Запуск бота
    bot.run(BOT_KEY, root_logger=True)


if __name__ == '__main__':
    run()
