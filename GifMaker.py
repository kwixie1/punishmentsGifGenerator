from PIL import Image, ImageDraw, ImageFont
from random import shuffle
from os import scandir
import textwrap
import json

def create_gif():
    """Создаём гифку, файл сохраняется в папке src/"""

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)["punishments"]  # Достаём все наказания из json файла

    img = Image.open("src/template.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("src/arialmt.ttf", 18)
    font2 = ImageFont.truetype("src/arialmt.ttf", 16)
    colors = {"невозможно": "#9d0000",  # HEX-коды цветов для текста в зависимости от сложности
              "сложно": "#e77763",
              "нормально": "#aab4c6",
              "легко": "#a2cf8f"}
    index = 0  # У нас будет нумерация кадров при сохранении

    for element in data:
        draw.rectangle((0, 120, 360, 240), (76, 76, 76))  # Заливкой прямоугольником очищаем кадр от следов прошлого

        text = "\n".join(textwrap.wrap(element["text"], width=25))  # Делаем версию с переносом текста
        x = (360 - draw.multiline_textbbox((0, 0), text, font)[2]) // 2  # Определяем x координату так, чтобы текст был в центре
        draw.multiline_text(  # Пишем многострочный (с переносами) текст на картинке
            xy=(x, 125), 
            text=text, 
            fill=colors[element["difficulty"]],
            font=font,
            align="center"
        )
        draw.text(  # Справа внизу пишем сложность с её цветом
            xy=(355 - (draw.textlength(element["difficulty"], font)), 220),  # Определяем оптимальную x координату
            text=element["difficulty"],
            font=font2,
            fill=colors[element["difficulty"]],
            align="right"
        )
        draw.text(  # Левее от прошлого, пишем дефолтный текст
            xy=(360 - (draw.textlength("Сложность:", font) + draw.textlength(element["difficulty"], font)), 220),
            text="Сложность:",
            font=font2,
            fill="white",
            align="right"
        )
        img.save(f"src/frames/{index}.png")  # Сохраняем получившийся кадр
        index += 1
        
    frames = [Image.open(file) for file in scandir("src/frames/")]  # берём сохранённые кадры и кидаем их в список 
    shuffle(frames)

    frames[0].save(  # Сохраняем это всё дело как гифку
        fp="punishments.gif",
        save_all=True,
        append_images=frames[1:],
        duration=0.7,
        loop=0,
        optimize=True
    )

if __name__ == "__main__":
    create_gif()