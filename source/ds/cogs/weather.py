"""
Файл для вывода погоды полученной от weather_api.py
"""
import discord
from discord.ext import commands
from discord import app_commands
from .utils import weather_api


# Основной класс
class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Создание группы команд 'weather'
    group = app_commands.Group(name="weather", description="Погода с "
                                                           "OpenWeatherAPI")

    # Вывод текущей погоды в embed
    @group.command(name='current', description='Показывает текущую '
                                               'погоду в заданном месте')
    @app_commands.describe(city='Город')
    async def current_weather(self, ctx, city: str):
        coords = weather_api.get_city_coords(city)
        request = weather_api.get_current_weather(coords)
        weather = weather_api.current_weather(request)
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title=str(weather[0] + ' ' + weather[1] + ' по местному времени'),
            description=f"""
            Погода: {weather[2]}
            Температура: {weather[3]} °C
            Ощущается как: {weather[4]} °C
            Минимальная температура: {weather[5]} °C
            Максимальная температура: {weather[6]} °C
            Влажность: {weather[7]} %
            Давление: {weather[8]} мм рт. ст.
            Ветер: {weather[9]}
            Видимость {weather[10]} м
            Рассвет: {weather[11]} по местному времени
            Закат: {weather[12]} по местному времени
            """
        )
        embed.set_thumbnail(url=weather[13])
        embed.set_footer(text=weather[14])
        await ctx.response.send_message(embed=embed, ephemeral=True)

    # Вывод почасовой погоды в embed
    @group.command(name='hourly', description='Показывает погоду по 3 '
                                              'часа на 5 дней вперед в '
                                              'заданном месте')
    @app_commands.describe(city='Город')
    @app_commands.describe(hour='Значение от 1 до 40')
    async def hourly_weather(self, ctx, city: str, hour: int):
        if hour in range(1, 41):
            # Так как получение 40 запросов за раз занимает время, а таймаут у
            # /команд довольно ограничен, создаётся временное сообщение, которое
            # позже заменяется на нужное
            await ctx.response.send_message('Пожалуйста подождите',
                                            ephemeral=True)
            coords = weather_api.get_city_coords(city)
            request = weather_api.get_hourly_weather(coords)
            response = weather_api.hourly_weather(request)
            weather = response[hour]
            embed = discord.Embed(
                colour=discord.Colour.blurple(),
                title=str(response[0] + ' ' + weather[0] +
                          ' по местному времени'),
                description=f"""
                        Погода: {weather[1]}
                        Температура: {weather[2]}°C
                        Ощущается как: {weather[3]}°C
                        Минимальная температура: {weather[4]}°C
                        Максимальная температура: {weather[5]}°C
                        Влажность: {weather[6]}%
                        Давление: {weather[7]}мм рт. ст.
                        Ветер: {weather[8]}
                        Видимость {weather[9]} м
                        Рассвет: {weather[10]} по местному времени
                        Закат: {weather[11]} по местному времени
                        """
            )
            embed.set_thumbnail(url=weather[12])
            embed.set_footer(text=str(str(hour) + '/40 ' + weather[13]))
            # Замена сообщения
            await ctx.edit_original_response(content='', embed=embed)
        else:
            await ctx.response.send_message('Доступное время от 1 до 40 '
                                            'включительно', ephemeral=True)


# Добавление в бота
async def setup(bot):
    await bot.add_cog(Weather(bot))
    print('Weather loaded')


# Убирание из бота
async def teardown(bot):
    await bot.remove_cog(Weather(bot))
    print('Weather unloaded')
