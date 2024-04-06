import tkinter as tk
from tkinter import filedialog
from image_editor import *
from PIL import Image, ImageDraw, ImageFont
import os

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Article Builder")
        self.geometry("500x500")

        self.create_label_entry("Заголовок:", "title")
        self.create_label_entry("Текст:", "main_text")

        self.backgrounds = {
            "Белый фон": "background_white.png",
            "Белый фон с изображением(мал.)": "background_white_with_image.png",
            "Белый фон с изображением(больш.)": "background_white_less.png",
            "Градиентный фон": "background_gradient.png",
            "Желтый фон": "background_yellow.png",
            "Желтый фон с изображением(больш.)": "background_yellow_less.png",
            "Желтый фон с изображением(мал.)": "background_yellow_with_image.png"
        }

        # Создаем выпадающий список для выбора фонового изображения
        self.create_label_combobox("Выберите фон:", "background_var", list(self.backgrounds.keys()))

        # Создаем кнопку для выбора изображения
        self.image_path = tk.StringVar()
        choose_image_button = ttk.Button(self, text="Выбрать изображение", command=self.choose_image)
        choose_image_button.pack(pady=10)

        # Создаем кнопку отправить
        submit_button = ttk.Button(self, text="Создать", command=self.submit)
        submit_button.pack(pady=10)

        # Создаем чекбокс
        self.arrow_var = tk.BooleanVar()
        arrow_checkbox = ttk.Checkbutton(self, text="Добавить стрелку", variable=self.arrow_var)
        arrow_checkbox.pack(pady=10)

        self.xbox_var = tk.BooleanVar()
        xbox_checkbox = ttk.Checkbutton(self, text="Вотермарк Xbox", variable=self.xbox_var)
        xbox_checkbox.pack(pady=10)

        self.ps_var = tk.BooleanVar()
        ps_checkbox = ttk.Checkbutton(self, text="Вотермарк PlayStation", variable=self.ps_var)
        ps_checkbox.pack(pady=10)

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

    def crop_and_merge(self, user_image_path, template_image_path, template_name):
        # Открываем изображения
        user_image = Image.open(user_image_path)
        template_image = Image.open(template_image_path)
        black_square = Image.open("images/black_square.png")

        # Вычисляем новые размеры, сохраняя соотношение сторон
        width, height = user_image.size
        if template_name == "background_white_with_image.png" or template_name == "background_yellow_with_image.png":
            new_width = width
            new_height = int(width / 3.04)
        elif template_name == "background_white_less.png" or template_name == "background_yellow_less.png":
            new_width = width
            new_height = int(width / 1.96)


        # Если новая высота больше исходной, то изменяем ширину
        if new_height > height:
            new_height = height
            new_width = int(height * 3.04)

        # Вычисляем координаты для обрезки
        left = (width - new_width) / 2
        top = (height - new_height) / 2
        right = (width + new_width) / 2
        bottom = (height + new_height) / 2

        # Обрезаем изображение пользователя
        user_image = user_image.crop((left, top, right, bottom))

        if template_name == "background_white_with_image.png":
            user_image = user_image.resize((1200, 395), Image.ANTIALIAS)
        else:
            user_image = user_image.resize((1200, 612), Image.ANTIALIAS)

        # Объединяем изображение пользователя с черным квадратом
        black_square.paste(user_image, (0, 0))

        # Объединяем получившееся изображение с шаблоном
        black_square.paste(template_image, (0, 0), template_image)

        # Сохраняем итоговое изображение во временный файл
        temp_path = "output/temp.png"
        black_square.save(temp_path)

        return temp_path

    def submit(self):
        # Получаем данные из полей для ввода
        title = self.title.get("1.0", 'end-1c')
        main_text = self.main_text.get("1.0", 'end-1c')

        # Определяем temp_path заранее
        temp_path = None

        # Получаем выбранное русское название
        selected_background = getattr(self, "background_var").get()

        # Используем словарь, чтобы найти соответствующее имя файла
        background_image = self.backgrounds[selected_background]

        # Если выбран один из специальных шаблонов, обрезаем и объединяем изображения
        if background_image in ["background_white_with_image.png", "background_white_less.png", "background_yellow_less.png", "background_yellow_with_image.png"]:
            user_image_path = self.image_path.get()
            template_image_path = f"images/{background_image}"
            temp_path = self.crop_and_merge(user_image_path, template_image_path, background_image)

            # Создаем объект ImageEditor для редактирования изображения
            editor = ImageEditor(temp_path)
        else:
            # Создаем объект ImageEditor для редактирования изображения
            editor = ImageEditor(f"images/{background_image}")

        # Загружаем шрифт (предполагается, что файл шрифта находится в той же директории)
        font_title_path = "fonts/segoe-ui-gras.ttf"
        font_text_path = "fonts/segoe-ui.ttf"
        font_size_title = 90
        font_size_main = 50

        # Создаем объекты font и draw
        font_title = ImageFont.truetype(font_title_path, font_size_title)
        font_text = ImageFont.truetype(font_text_path, font_size_main)

        # Разбиваем текст на строки
        title = self.wrap_text(title, 960, font_title, editor.image)
        main_text = self.wrap_text(main_text, 960, font_text, editor.image)

        # Рассчитываем высоту текста заголовка
        title_height = len(title.split('\n')) * font_size_title

        if background_image != "background_white_less.png" and background_image != "background_yellow_less.png":
            if main_text == "":
                if background_image != "background_yellow.png" or background_image != "background_yellow_with_image.png":
                    editor.add_gradient_text(title, (50, 460), font_title_path, font_size_title)
                else:
                    editor.add_text(title, (50, 460), font_title_path, font_size_title, (28, 28, 28))
            elif title == "":
                editor.add_text(main_text, (50, 560), font_text_path, font_size_main, (32,32,32))
            else:
                if background_image != "background_yellow.png" or background_image != "background_yellow_with_image.png":
                    editor.add_gradient_text(title, (50, 300), font_title_path, font_size_title)
                    editor.add_text(main_text, (50, 300 + title_height + 80), font_text_path, font_size_main,
                                    (32, 32, 32))
                else:
                    editor.add_text(title, (50, 300), font_title_path, font_size_title, (28, 28, 28))
                    editor.add_text(main_text, (50, 300 + title_height + 80), font_text_path, font_size_main,
                                    (32, 32, 32))

        else:
            if main_text == "":
                editor.add_gradient_text(title, (50, 490), font_title_path, font_size_title)
            elif title == "":
                if background_image != "background_yellow_less.png":
                    editor.add_text(main_text, (50, 590), font_text_path, font_size_main, (32,32,32))
                else:
                    editor.add_text(title, (50, 590), font_title_path, font_size_title, (28, 28, 28))
            else:
                if background_image != "background_yellow_less.png":
                    editor.add_gradient_text(title, (50, 500), font_title_path, font_size_title)
                    editor.add_text(main_text, (50, 500 + title_height + 80), font_text_path, font_size_main, (32,32,32))
                else:
                    editor.add_text(title, (50, 500), font_title_path, font_size_title, (28, 28, 28))
                    editor.add_text(main_text, (50, 500 + title_height + 80), font_text_path, font_size_main, (32,32,32))

        if self.arrow_var.get():
            # Если выбран, накладываем изображение стрелки
            arrow_image = Image.open("images/arrow.png")
            new_size = (300, 300)  # Новый размер в пикселях
            arrow_image = arrow_image.resize(new_size, Image.ANTIALIAS)
            editor.image.paste(arrow_image, (440, 750), arrow_image)

        if self.xbox_var.get():
            xbox_image = Image.open("images/xbox4joy.png")
            new_size = (220, 220)  # Новый размер в пикселях
            xbox_image = xbox_image.resize(new_size, Image.ANTIALIAS)
            editor.image.paste(xbox_image, (470, 1040), xbox_image)

        if self.ps_var.get():
            ps_image = Image.open("images/ps4joy.png")
            new_size = (220, 220)  # Новый размер в пикселях
            ps_image = ps_image.resize(new_size, Image.ANTIALIAS)
            editor.image.paste(ps_image, (470, 1040), ps_image)

        # Сохраняем изображение с уникальным именем файла
        output_path = "output/output.png"
        i = 1
        while os.path.exists(output_path):
            output_path = f"output/output{i}.png"
            i += 1

        editor.save(output_path)

        # Если существует временный файл, удаляем его
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    app = Application()
    app.mainloop()
