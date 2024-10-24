import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from collections import Counter

class InsuranceContract:
    def __init__(self, cost_of_insurance, insurance_type, agent_name):
        self.cost_of_insurance = cost_of_insurance
        self.insurance_type = insurance_type
        self.agent_name = agent_name

    def __str__(self):
        return f"{self.cost_of_insurance}, {self.insurance_type}, {self.agent_name}"

    @staticmethod
    def load_contracts(filename):
        contracts = []
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        contracts.append(InsuranceContract(float(parts[0]), parts[1], parts[2]))
        except FileNotFoundError:
            messagebox.showerror("Ошибка", "Файл не найден.")
        except UnicodeDecodeError:
            messagebox.showerror("Ошибка", "Ошибка декодирования файла. Проверьте кодировку.")
        except ValueError:
            messagebox.showerror("Ошибка", "Ошибка преобразования данных. Проверьте формат файла.")
        return contracts

class InsuranceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Страховые Договоры")
        self.root.geometry('800x600')
        self.root.configure(background="#0f0f38")

        # Создание фрейма для кнопок
        button_frame = ttk.Frame(root, padding="10")
        button_frame.pack(side=tk.TOP, fill=tk.X)

        # Кнопка загрузки договоров
        self.load_button = ttk.Button(button_frame, text="Загрузить договоры", command=self.load_contracts)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Кнопка сегментации по видам страхования
        self.type_button = ttk.Button(button_frame, text="Сегментация по видам страхования", command=lambda: self.segment_by_type())
        self.type_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Кнопка сегментации по агентам
        self.agent_button = ttk.Button(button_frame, text="Сегментация по страховым агентам", command=lambda: self.segment_by_agent())
        self.agent_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Создание фрейма для таблицы и скроллбара
        table_frame = ttk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создание Treeview для отображения данных
        self.tree = ttk.Treeview(table_frame, columns=("Insurance_agents", "Types_insurance", "Cost_insurance"), show="headings")
        self.tree.heading("Insurance_agents", text="Страховые агенты")
        self.tree.heading("Types_insurance", text="Виды страхования")
        self.tree.heading("Cost_insurance", text="Стоимость страхования")
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Создаем вертикальный скроллбар
        vert_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        vert_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=vert_scrollbar.set)

        self.contracts = []

    def load_contracts(self):
        self.contracts = InsuranceContract.load_contracts('contracts.txt')
        self.populate_treeview()
        messagebox.showinfo("Успех", f"Загружено {len(self.contracts)} договоров.")

    def populate_treeview(self):
        # Очищаем существующие данные в Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        for contract in self.contracts:
            self.tree.insert("", tk.END, values=(contract.agent_name, contract.insurance_type, contract.cost_of_insurance))

    def segment_by_type(self):
        types = [contract.insurance_type for contract in self.contracts]
        type_counts = Counter(types)
        self.visualize(type_counts, "type")

    def segment_by_agent(self):
        agents = [contract.agent_name for contract in self.contracts]
        agent_counts = Counter(agents)
        self.visualize(agent_counts, "agent")

    def visualize(self, data, name):
        labels = data.keys()
        sizes = data.values()
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Чтобы круговая диаграмма выглядела как круг
        if name == "type":
            plt.title('Визуализация по видам страхования')
        elif name == "agent":
            plt.title('Визуализация по страховым агентам')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = InsuranceApp(root)
    root.mainloop()