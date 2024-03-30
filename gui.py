import os
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from image_editor import *
from calculator import CalculatorWindow


class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Article Builder")
        self.geometry("500x600")

        self.create_label_entry("Название:", "game_name")
        self.create_label_combobox("Русский язык:", "russian_language",
                                   ["СУБТИТРЫ", "ПОЛНАЯ ЛОКАЛИЗАЦИЯ", "БЕЗ ПЕРЕВОДА"])
        self.create_label_combobox("Платформы:", "platforms", ["Xbox ONE", "Xbox Series X", "Xbox Series S", "One,Series S|X"])
        self.create_label_combobox("Версия игры:", "game_version", ["Standard Edition", "Deluxe Edition", "Ultimate Edition"])
        self.create_label_entry("Цена:", "game_price")
        self.create_label_entry("Скидка:", "discount")
        self.create_label_entry("Дата окончания скидки:", "discount_end_date")

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
        entry_var = tk.StringVar()
        setattr(self, entry_var_name, entry_var)
        entry = ttk.Entry(self, textvariable=entry_var)
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

    def submit(self):
        # Получаем данные из полей для ввода
        game_link = self.game_link.get()
        game_name = self.game_name.get()
        russian_language = self.russian_language.get()
        platforms = self.platforms.get()

        game_version = self.game_version.get()
        game_price = self.game_price.get()
        discount = self.discount.get()
        discount_end_date = self.discount_end_date.get()

        discount_position_square = [3000, 3620]
        discount_position_text = [3030, 3675]



        # Open the background image
        background = Image.open(self.image_path.get())

        # Изменяем размер фонового изображения
        width_ratio = 4096 / background.width
        height_ratio = 3565 / background.height
        ratio = max(width_ratio, height_ratio)
        new_width = int(background.width * ratio)
        new_height = int(background.height * ratio)
        background = background.resize((new_width, new_height))

        # Обрезаем фоновое изображение
        left_margin = (background.width - 4096) / 2
        top_margin = (background.height - 3565) / 2
        background = background.crop((left_margin, top_margin, left_margin + 4096, top_margin + 3565))

        # Создаем черное изображение нужного размера
        black_square = Image.new('RGB', (4096, 4857 - 3565), color='black')

        # Объединяем фоновое изображение и черный квадрат
        final_image = Image.new('RGB', (4096, 4857))
        final_image.paste(background, (0, 0))
        final_image.paste(black_square, (0, 3565))



        # Сохраняем изображение с уникальным именем файла
        output_path = "output/output.png"
        i = 1
        while os.path.exists(output_path):
            output_path = f"output/output{i}.png"
            i += 1

        final_image.save(output_path)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
