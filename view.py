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
        super().__init__()
        self.controller = controller

        # установка верхнего фрейма для кнопок-слоев
        self.layers_buttons_frame = ttk.Frame(self, height=60, padding=[8, 8])
        self.layers_buttons_frame.pack(anchor=N, fill=X)
        self.layers_buttons_frame.pack_propagate(False)

        # отрисовка кнопок-слоев в верхнем фрейме
        self._make_add_linear_button()
        self._make_add_relu_button()

        # установка фрейма для слоев
        self.layers_frame = ttk.Frame(self, height=200, width=200, relief=RAISED, border=1)
        self.layers_frame.pack(anchor=N, padx=20, pady=100)

        # сетка для слоев
        self.row = 0
        self.col = 0
        self.layers_frame.rowconfigure(index=self.row, weight=1)
        self.layers_frame.columnconfigure(index=self.col, weight=1)

    def print_new_layer(self, name_layer):
        new_layer = LayerWidgetView(master=self.layers_frame, name_layer=str(name_layer))
        new_layer.pack_widget(col=self.col)     # слой помещается в текущий столбец
        self.col += 1       # теперь столбцов нужно больше
        self.layers_frame.columnconfigure(index=self.col, weight=1)     # переопределяем количество столбцов

    def _make_add_linear_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='Linear',
                                   command=self.controller.on_add_linear_button_click)
        linear_button.pack(side=LEFT)

    def _make_add_relu_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='ReLU',
                                   command=self.controller.on_add_relu_button_click)
        linear_button.pack(side=LEFT, padx=5)


class DataView(ttk.Frame):
    """
    Вкладка загрузки данных.
    """

    def __init__(self, master):
        super().__init__()
        pass


class HyperView(ttk.Frame):
    """
    Вкладка подбора гиперпараметров.
    """

    def __init__(self, master):
        super().__init__()
        pass


class ValidationView(ttk.Frame):
    """
    Вкладка оценки качества модели.
    """

    def __init__(self, master):
        super().__init__()
        pass


class LayerWidgetView:
    """
    Графическое отображение виджета для любого слоя в виде рамки на главном окне
    """

    def __init__(self, master, name_layer):
        super().__init__()

        # рамка слоя, мастер для всех внутренних компонентов
        self.layer_frame = ttk.Frame(master, relief=RAISED, border=1, width=150, height=200)

        # виджет-надпись отображает имя слоя
        self.text_layer = ttk.Label(self.layer_frame, relief=RAISED, text=name_layer, background='gray90')

    def pack_widget(self, col):
        """
        Располагает виджет. Полезно, потому что можно передавать координаты в
        этот метод из главного окна и друг за другом выстраивать слои
        """

        self.layer_frame.grid(row=0, column=col, padx=20)

        self.layer_frame.pack_propagate(False)

        self.text_layer.pack(fill=X, padx=1, pady=1)
