import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from image_editor import *
from PIL import Image, ImageDraw, ImageFont
import textwrap

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Article Builder")
        self.geometry("500x600")

        self.create_label_entry("Заголовок:", "title")
        self.create_label_entry("Текст:", "main_text")

        # Создаем кнопку для выбора изображения
        self.image_path = tk.StringVar()
        choose_image_button = ttk.Button(self, text="Выбрать изображение", command=self.choose_image)
        choose_image_button.pack(pady=10)

        # Создаем кнопку отправить
        submit_button = ttk.Button(self, text="Создать", command=self.submit)
        submit_button.pack(pady=10)

    def create_label_entry(self, label_text, entry_var_name):
        # Создаем метку
        label = ttk.Label(self, text=label_text)
        label.pack(fill='x', padx=5, pady=5)

        # Создаем поле для ввода
        entry = tk.Text(self, height=4, width=50)
        setattr(self, entry_var_name, entry)
        entry.pack(fill='x', padx=5)

    def create_label_combobox(self, label_text, combobox_var_name, values):
        # Создаем метку
        label = ttk.Label(self, text=label_text)
        label.pack(fill='x', padx=5, pady=5)

        # Создаем выпадающий список
        combobox_var = tk.StringVar()
        setattr(self, combobox_var_name, combobox_var)
        combobox = ttk.Combobox(self, textvariable=combobox_var, values=values)
        combobox.pack(fill='x', padx=5)

    def choose_image(self):
        # Открываем диалог выбора файла и сохраняем путь к выбранному файлу
        file_path = filedialog.askopenfilename()
        self.image_path.set(file_path)

    def wrap_text(self, text, max_width, font, image):
        words = text.split()
        lines = []
        current_line = []
        current_width = 0

        draw = ImageDraw.Draw(image)  # Создаем объект draw здесь

        for word in words:
            word_width, _ = draw.textsize(word, font=font)
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width

        lines.append(' '.join(current_line))  # add the last line
        return '\n'.join(lines)

    def submit(self):
        # Получаем данные из полей для ввода
        title = self.title.get("1.0", 'end-1c')
        main_text = self.main_text.get("1.0", 'end-1c')

        # Создаем объект ImageEditor для редактирования изображения
        editor = ImageEditor("images/background_white.png")

        # Загружаем шрифт (предполагается, что файл шрифта находится в той же директории)
        font_title_path = "fonts/segoe-ui-gras.ttf"
        font_text_path = "fonts/segoe-ui.ttf"
        font_size = 45

        # Создаем объекты font и draw
        font_title = ImageFont.truetype(font_title_path, font_size)
        font_text = ImageFont.truetype(font_text_path, font_size)

        # Разбиваем текст на строки
        title = self.wrap_text(title, 1000, font_title, editor.image)
        main_text = self.wrap_text(main_text, 1000, font_text, editor.image)

        # Добавляем заголовок и основной текст на изображение
        # Координаты (x, y) определяют местоположение текста
        editor.add_gradient_text(title, (50, 50), font_title_path, font_size)
        editor.add_text(main_text, (50, 100), font_text_path, font_size, "black")

        # Сохраняем изображение с уникальным именем файла
        output_path = "output/output.png"
        i = 1
        while os.path.exists(output_path):
            output_path = f"output/output{i}.png"
            i += 1

        editor.save(output_path)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
