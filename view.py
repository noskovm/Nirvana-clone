from tkinter import *
from tkinter import ttk
import sv_ttk


class View(Tk):
    """
    Представление. Содержит 4 вкладки для разных этапов задачи
    Загрузка данных, построение модели, перебор гиперпараметров, оценка качества
    _______________________________________________________
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

        # некоторые беды со стилем(чтобы убрать пунктир)
        style = ttk.Style()
        style.layout("Tab",
                     [('Notebook.tab', {'sticky': 'nswe', 'children':
                      [('Notebook.padding', {'side': 'top', 'sticky': 'nswe', 'children':
                       [('Notebook.label', {'side': 'top', 'sticky': ''})],
                                             })],
                                        })]
                     )

        self.data_view = DataView(container=self.tub)
        self.network_view = NetworkView(container=self.tub, controller=self.controller)
        self.hyper_view = HyperView(container=self.tub)
        self.validation_view = ValidationView(container=self.tub)

        self.tub.add(self.data_view, text='DATA')
        self.tub.add(self.network_view, text='NETWORK')
        self.tub.add(self.hyper_view, text='HYPERPARAMETERS')
        self.tub.add(self.validation_view, text='VALIDATION')

        self.tub.pack(expand=True, fill=BOTH)

    def main(self):
        self.mainloop()


class NetworkView(ttk.Frame):
    """
    Вкладка построения графа вычислений(нейронной сети).
    """

    def __init__(self, container, controller):
        super().__init__()
        self.controller = controller

        # отрисовка главных кнопок
        self._make_add_layer_button()
        self._make_train_button()

    def print_new_layer(self, name_layer):
        """
        :param name_layer: имя слоя для отображения
        """

        new_layer = LayerWidgetView(container=self, name_layer=str(name_layer))
        new_layer.pack()

    def _make_train_button(self):
        train_button = ttk.Button(self, text='TRAIN')
        train_button.pack(anchor='nw')

    def _make_add_layer_button(self):
        train_button = ttk.Button(self, text='add layer', command=self.controller.on_add_layer_button_click)
        train_button.pack()


class DataView(ttk.Frame):
    """
    Вкладка загрузки данных.
    """

    def __init__(self, container):
        super().__init__()
        pass


class HyperView(ttk.Frame):
    """
    Вкладка подбора гиперпараметров.
    """

    def __init__(self, container):
        super().__init__()
        pass


class ValidationView(ttk.Frame):
    """
    Вкладка оценки качества модели.
    """

    def __init__(self, container):
        super().__init__()
        pass


class LayerWidgetView:
    """
    Графическое отображение виджета для любого слоя в виде рамки на главном окне
    """

    def __init__(self, container, name_layer):
        super().__init__()

        self.frame = ttk.Frame(container, relief=RAISED, border=1)

        # виджет-рамка отображает все параметры слоя(размер входа, выхода; гиперпараметры)

        # виджет-надпись отображает имя слоя
        self.lab = ttk.Label(self.frame, relief=RAISED, text=name_layer)

    def pack(self):
        """
        Располагает виджет. Полезно, потому что можно передавать координаты в
        этот метод из главного окна и друг за другом выстраивать слои
        """

        self.frame.place(x=300, y=300, width=200, height=200)
        self.lab.pack(fill=X, padx=1, pady=1)
