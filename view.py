from tkinter import *
from tkinter import ttk
import sv_ttk


class View(Tk):
    """
    Представление. Содержит 4 вкладки для разных этапов задачи
    Загрузка данных, построение модели, перебор гиперпараметров, оценка качества
    ____________________________________________________________________________
    DATA | NETWORK | HYPERPARAMETERS | VALIDATION
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # конфигурация окна
        sv_ttk.set_theme("light")
        self.title('Главная рабочая область')
        self.geometry('1800x900')

        # инициализация и упаковка вкладок
        self.tub = ttk.Notebook(self)
        self.tub.pack(expand=True, fill=BOTH)

        # некоторые беды со стилем(чтобы убрать пунктир)
        style = ttk.Style()
        style.layout("Tab",
                     [('Notebook.tab', {'sticky': 'nswe', 'children':
                      [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                       [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                                })],
                                        })]
                     )

        self.data_view = DataView(master=self.tub)
        self.network_view = NetworkView(master=self.tub, controller=self.controller)
        self.hyper_view = HyperView(master=self.tub)
        self.validation_view = ValidationView(master=self.tub)

        self.data_view.pack(fill=BOTH, expand=True)
        self.network_view.pack(fill=BOTH, expand=True)
        self.hyper_view.pack(fill=BOTH, expand=True)
        self.validation_view.pack(fill=BOTH, expand=True)

        self.tub.add(self.data_view, text='DATA')
        self.tub.add(self.network_view, text='NETWORK')
        self.tub.add(self.hyper_view, text='HYPERPARAMETERS')
        self.tub.add(self.validation_view, text='VALIDATION')

    def main(self):
        self.mainloop()


class NetworkView(ttk.Frame):
    """
    Вкладка построения графа вычислений(нейронной сети).
    """

    def __init__(self, master, controller):
        super().__init__(master)
        self.controller = controller

        # установка фрейма для кнопок-слоев
        self.layers_buttons_frame = ttk.Frame(self, height=60, padding=[8, 8])
        self.layers_buttons_frame.pack(anchor=N, fill=X)

        # отрисовка кнопок-слоев
        self._make_add_linear_button()
        self._make_add_ReLU_button()

    def print_new_layer(self, name_layer):
        new_layer = LayerWidgetView(master=self, name_layer=str(name_layer))
        new_layer.pack()

    def _make_add_linear_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='Linear',
                                   command=self.controller.on_add_linear_button_click)
        linear_button.pack(side=LEFT)

    def _make_add_ReLU_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='ReLU',
                                   command=self.controller.on_add_ReLU_button_click)
        linear_button.pack(side=LEFT, padx=5)



class DataView(ttk.Frame):
    """
    Вкладка загрузки данных.
    """

    def __init__(self, master):
        super().__init__(master)
        pass


class HyperView(ttk.Frame):
    """
    Вкладка подбора гиперпараметров.
    """

    def __init__(self, master):
        super().__init__(master)
        pass


class ValidationView(ttk.Frame):
    """
    Вкладка оценки качества модели.
    """

    def __init__(self, master):
        super().__init__(master)
        pass


class LayerWidgetView(ttk.Frame):
    """
    Графическое отображение виджета для любого слоя в виде рамки на главном окне
    """

    def __init__(self, master, name_layer):
        super().__init__(master)

        self.config(relief=RAISED, border=1)

        # виджет-надпись отображает имя слоя
        self.lab = ttk.Label(self, relief=RAISED, text=name_layer)

    def pack(self):
        """
        Располагает виджет. Полезно, потому что можно передавать координаты в
        этот метод из главного окна и друг за другом выстраивать слои
        """

        self.place(x=300, y=300, width=200, height=200)
        self.lab.pack(fill=X, padx=1, pady=1)
