from PIL import Image, ImageDraw, ImageFont
from tkinter import ttk

class ImageEditor:
    def __init__(self, template_path):
        self.image = Image.open(template_path)
        self.draw = ImageDraw.Draw(self.image)

    def add_text(self, text, position, font_path, font_size, color):
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(self.image)

        lines = text.split('\n')
        y_text = position[1]
        for line in lines:
            width, height = draw.textsize(line, font)
            draw.text((position[0], y_text), line, font=font, fill=color)
            y_text += height

    def add_text_with_shadow(self, text, position, font_path, font_size):
        x, y = position
        font = ImageFont.truetype(font_path, font_size)

        # Рисуем тень
        shadow_color = "gray"
        self.draw.text((x-3, y-3), text, fill=shadow_color, font=font)

        # Рисуем основной текст поверх тени
        text_color = "black"
        self.draw.text(position, text, fill=text_color, font=font)

    def create_gradient(self, width, height, start_color, end_color):
        base = Image.new('RGB', (width, height), start_color)
        top = Image.new('RGB', (width, height), end_color)
        mask = Image.new('L', (width, height))
        mask_data = []
        for y in range(height):
            for x in range(width):
                mask_data.append(int(255 * (x / width)))
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base

    def add_gradient_text(self, text, position, font_path, font_size):
        x, y = position
        font = ImageFont.truetype(font_path, font_size)

        lines = text.split('\n')
        for line in lines:
            # Получаем размеры текста
            text_width, text_height = font.getsize(line)

            # Создаем изображение с градиентом
            gradient = self.create_gradient(text_width, text_height, (69, 116, 233), (65, 189, 240))

            # Создаем новое изображение для текста
            text_image = Image.new('RGBA', (text_width, text_height), (0, 0, 0, 0))
            text_draw = ImageDraw.Draw(text_image)

            # Рисуем текст белым цветом (это будет использоваться как маска)
            text_draw.text((0, 0), line, font=font, fill=(255, 255, 255))

            # Накладываем градиент на текст с использованием текста в качестве маски
            self.image.paste(gradient, (x, y), mask=text_image)

            # Обновляем позицию y для следующей строки
            y += text_height

    def save(self,output_path):
         self.image.save(output_path,'PNG')
