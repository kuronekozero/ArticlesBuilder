import math
import tkinter as tk
import os
import json

class CalculatorWindow(tk.Toplevel):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.title("PS Store Reseller App")
        self.geometry("500x200")

        # Создаем переменные для чекбоксов
        self.var_tr = tk.IntVar()
        self.var_ua = tk.IntVar()

        # Создаем чекбоксы
        c1 = tk.Checkbutton(self, text='Турция', variable=self.var_tr, onvalue=1, offvalue=0)
        c1.pack()
        c2 = tk.Checkbutton(self, text='Украина', variable=self.var_ua, onvalue=1, offvalue=0)
        c2.pack()

        # Создаем поле для ввода цены
        self.price_entry = tk.Entry(self)
        self.price_entry.pack()

        # Создаем поле для вывода результата
        self.result_entry = tk.Entry(self)
        self.result_entry.pack()

        # Создаем кнопку "Подсчитать"
        calculate_button = tk.Button(self, text="Подсчитать", command=self.calculate)
        calculate_button.pack(pady=10)

    def load_coefficients(self, region):
        filename = f"coefficients{region}.json"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                coefficients = json.load(file)
        else:
            coefficients = None
        return coefficients

    def convert_price(self, price_in_currency, region):
        # Загружаем коэффициенты
        coefficients = self.load_coefficients(region)
        if coefficients is None:
            print(f"Не удалось загрузить коэффициенты для региона {region}")
            return None

        # Округляем цену в большую сторону до целых единиц
        price_in_currency = math.ceil(price_in_currency)

        # Выбираем коэффициент для конвертации в рубли в зависимости от цены
        if region == "tr":
            if price_in_currency < 100:
                coefficient = coefficients[f"less100{region}"]
            elif price_in_currency < 699:
                coefficient = coefficients[f"less699{region}"]
            elif price_in_currency < 1199:
                coefficient = coefficients[f"less1199{region}"]
            elif price_in_currency < 1799:
                coefficient = coefficients[f"less1799{region}"]
            else:
                coefficient = coefficients[f"more1799{region}"]
        elif region == "ua":
            if price_in_currency < 300:
                coefficient = coefficients[f"less300{region}"]
            elif price_in_currency < 1499:
                coefficient = coefficients[f"less1499{region}"]
            elif price_in_currency < 1999:
                coefficient = coefficients[f"less1999{region}"]
            else:
                coefficient = coefficients[f"more1999{region}"]

        if region == "tr" and coefficient != coefficients[f"less100{region}"]:
            # Прибавляем процент к цене
            price_in_currency += price_in_currency * coefficients[f"percent{region}"]
        elif region == "ua" and coefficient != coefficients[f"less300{region}"]:
            # Прибавляем процент к цене
            price_in_currency += price_in_currency * coefficients[f"percent{region}"]

        # Округляем цену в большую сторону до целых единиц или десятков в зависимости от региона
        if region == "ua":
            price_in_currency = math.ceil(price_in_currency / 10.0) * 10
        else:
            price_in_currency = math.ceil(price_in_currency)

        # Конвертируем цену в рубли
        price_in_rubles = price_in_currency * coefficient

        # Округляем цену в большую сторону до десятков
        price_in_rubles = math.ceil(price_in_rubles / 10.0) * 10

        return price_in_rubles

    def calculate(self):
        # Получаем значение цены из поля ввода
        price_in_currency = float(self.price_entry.get())

        # Определяем регион в зависимости от выбранного чекбокса
        if self.var_tr.get() == 1:
            region = "tr"
        elif self.var_ua.get() == 1:
            region = "ua"
        else:
            print("Не выбран регион")
            return

        # Вызываем функцию подсчета цены
        price_in_rubles = self.convert_price(price_in_currency, region)

        # Выводим результат в поле для вывода результата
        self.result_entry.delete(0, tk.END)  # очищаем поле
        self.result_entry.insert(0, price_in_rubles)  # вставляем результат






