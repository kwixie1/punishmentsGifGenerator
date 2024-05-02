from nextcord.ext import commands
from dotenv import load_dotenv
import GifMaker
import nextcord
import json
import os

load_dotenv()
bot_token = os.getenv("TOKEN")  # Берём токен из файла .env

client = commands.Bot()


@client.event
async def on_ready():
    print("online")


@client.slash_command()
async def info(interaction: nextcord.Interaction):
    """Команда с полезной информацией, ничего более"""

    await interaction.send("""# Информация про бота-генератора
В основном бот создан для одной цели - удобное создание кастомных гифок для "наказаний".
Хоть функционал и очень узконаправлен, у него есть пару нюансов, о которых лучше рассказать:

## Для создания гифки, вам необходимо знать:
- Сначала, осуществляется сбор наказаний с помощью команды `/add_punishment`. 
    В аргументах команды необходимо будет указать сам текст и сложность ЦИФРОЙ (про это будет ниже).
    Весь текст сохраняется в одном json файле, с которым особых манипуляций через бота не предусмотрено.
- Максимальная длина наказания - 150 символов
- Когда собрано достаточно наказаний, можно использовать команду `/create_gif`, и создать гифку.
        
### Про сложность
Сложность я отметила цифрами, так как это легче, понятнее и удобнее (но нужно знать, что каждая из них значит)
    1 - Невозможно
    2 - Сложно
    3 - Нормально (дефолт)
    4 - Легко""")


@client.slash_command()
async def add_punishment(interaction: nextcord.Interaction, text: str, difficulty: int = 3):
    """Команда для добавления наказаний в json файлик"""

    if len(text) > 100:  # Возвращаемся, если текст длиннее нужного
        await interaction.send("Слишком много текста! Не воспринимаю.")
        return
    
    popaorla = {1: "невозможно", 2: "сложно", 3: "нормально", 4: "легко"}

    if difficulty not in popaorla:  # Возвращаемся, если указана неправильная сложность
        await interaction.send("Такой сложности не существует, загляни в `/info`", ephemeral=True)
        return
    
    with open("data.json", "r", encoding="utf-8") as f:
        idk = json.load(f)  # Подгружаем файл

    idk["punishments"].append({"text": text, "difficulty": popaorla[difficulty]})  # Обновляем содержимое (добавлям наказание)

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(idk, f, indent=4)  # Закидываем обновлённый json

    await interaction.send(f"Наказание `{text}` со сложностью `{popaorla[difficulty]}` было сохранено!\n" +
    f"{len(idk['punishments'])} наказаний уже записано")


@client.slash_command()
async def create_gif(interaction: nextcord.Interaction):
    """Создаём саму гифку"""
    GifMaker.create_gif()  # В файле модуля можно посмотреть, что делает функция

    await interaction.send(
        content="Готово!",
        file=nextcord.File("punishments.gif")  # Отправляем гифку, которую сохранила функция create_gif()
    )
    

if __name__ == "__main__":
    client.run(bot_token)