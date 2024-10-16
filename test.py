"""
Задание на л.р. №8 ООП 24
Требуется написать объектно-ориентированную программу с графическим интерфейсом в соответствии со своим вариантом.
В программе должны быть реализованы минимум один класс, три атрибута, четыре метода (функции).
Ввод данных из файла с контролем правильности ввода.
Базы данных использовать нельзя. При необходимости сохранять информацию в виде файлов, разделяя значения запятыми или пробелами.
Для GUI использовать библиотеку tkinter.
Вариант 13
Объекты – экспонаты на выставке
Функции:	сегментация полного списка экспонатов по категориям
визуализация предыдущей функции в форме круговой диаграммы
сегментация полного списка экспонатов по фирмам
визуализация предыдущей функции в форме круговой диаграммы
"""
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import ttk
import csv
from collections import defaultdict
import matplotlib.pyplot as plt


class Exposition:
    def __init__(self):
        self.items = []
        self.categories = defaultdict(list)
        self.firms = defaultdict(list)

    def load_items(self, filename):
        try:
            with open(filename, 'r', encoding='cp1251') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 3:
                        self.items.append(row)
                    else:
                        raise ValueError("Неверный формат файла")
        except Exception as e:
            raise e

    def save_items(self, filename):
        try:
            with open(filename, 'w', encoding='cp1251', newline='') as file:
                writer = csv.writer(file)
                for item in self.items:
                    writer.writerow(item)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")

    def add_item(self, name, category, firm):
        self.items.append([name, category, firm])
        self.segment_by_category()
        self.segment_by_firm()

    def segment_by_category(self):
        self.categories.clear()
        for item in self.items:
            self.categories[item[1]].append(item)

    def segment_by_firm(self):
        self.firms.clear()
        for item in self.items:
            self.firms[item[2]].append(item)


class GUI:
    def __init__(self, root):
        self.exposition = Exposition()
        self.root = root
        self.root.title("Выставка экспонатов")
        self.root.geometry('%dx%d+%d+%d' % (1585, 900, 150, 50))
        self.setup_ui()
        self.filename = ""

    def setup_ui(self):

        self.load_button = tk.Button(self.root, text="Загрузить файл", command=self.load_file)
        self.load_button.pack(pady=10)

        self.add_button = tk.Button(self.root, text="Добавить экспонат", command=self.add_item_dialog)
        self.add_button.pack(pady=10)

        self.segment_cat_button = tk.Button(self.root, text="Сегментировать по категориям", command=self.segment_by_category)
        self.segment_cat_button.pack(pady=10)

        self.segment_firm_button = tk.Button(self.root, text="Сегментировать по фирмам", command=self.segment_by_firm)
        self.segment_firm_button.pack(pady=10)


        self.table = ttk.Treeview(self.root, columns=('name', 'category', 'firm'), show='headings', height=30)
        self.table.heading('name', text='Название')
        self.table.heading('category', text='Категория')
        self.table.heading('firm', text='Фирма')
        self.table.pack(expand=1, fill='x')


    def load_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            try:
                self.filename = file_path
                self.exposition.load_items(file_path)
                self.update_table()
                messagebox.showinfo("Успех", "Файл успешно загружен!")
            except Exception as e:
                messagebox.showerror("Ошибка", str(e))

    def update_table(self):
        for row in self.table.get_children():
            self.table.delete(row)
        for item in self.exposition.items:
            self.table.insert('', 'end', values=item)

    def add_item_dialog(self):
        name = simpledialog.askstring("Название", "Введите название экспоната:\t\t\t", parent=root)
        category = simpledialog.askstring("Категория", "Введите категорию экспоната:\t\t\t", parent=root)
        firm = simpledialog.askstring("Фирма", "Введите фирму экспоната:\t\t\t", parent=root)
        if name and category and firm:
            self.exposition.add_item(name, category, firm)
            self.update_table()
            self.exposition.save_items(self.filename)

    def segment_by_category(self):
        self.exposition.segment_by_category()
        self.show_pie_chart(self.exposition.categories, "Сегментация по категориям")

    def segment_by_firm(self):
        self.exposition.segment_by_firm()
        self.show_pie_chart(self.exposition.firms, "Сегментация по фирмам")

    def show_pie_chart(self, data, title):
        labels = data.keys()
        sizes = [len(v) for v in data.values()]
        plt.figure(figsize=(9, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title(title)
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
