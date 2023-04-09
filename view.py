from tkinter import *
from tkinter import ttk


class View(Tk):
    """
    Представление. Содержит 4 вкладки для разных этапов задачи
    Загрузка данных, построение модели, перебор гиперпараметров, оценка качества
    _______________________________________________________
    DATA | NETWORK | HYPERPARAMETERS | TEST
    """

    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        # конфигурация окна
        self.title('Главная рабочая область')
        self.geometry('1800x900')

        # вкладки
        self.tub = ttk.Notebook(self)
        self.data_view = DataView(container=self.tub)
        self.network_view = NetworkView(container=self.tub, controller=self.controller)

        self.tub.add(self.data_view, text='DATA')
        self.tub.add(self.network_view, text='NETWORK')

        self.tub.pack(expand=True, fill=BOTH)

    def main(self):
        self.mainloop()


class NetworkView(ttk.Frame):
    """
    То, что видит пользователь. Главная рабочая область
    """

    def __init__(self, container, controller):
        super().__init__()
        self.controller = controller

        # отрисовка главных кнопок
        self._make_add_layer_button()
        self._make_train_button()

    def _print_new_layer(self, name_layer):
        new_layer = LayerWidgetView(root_widget=self, name_layer=str(name_layer))
        new_layer.pack()

    def _make_train_button(self):
        train_button = ttk.Button(self, text='TRAIN')
        train_button.pack(anchor='nw')

    def _make_add_layer_button(self):
        train_button = ttk.Button(self, text='add layer', command=self.controller.on_add_layer_button_click)
        train_button.pack()


class LayerWidgetView:
    """
    Графическое отображение виджета для абстрактного слоя в виде рамки на главном окне
    """

    def __init__(self, root_widget, name_layer):
        super().__init__()

        self.root = root_widget  # нужно знать класс, где отображать виджет

        # начальное позиционирование виджета
        self.__winX = 300
        self.__winY = 300

        # запоминаем последние координаты для реализации движения
        self.__lastX = 0
        self.__lastY = 0

        # виджет-рамка отображает все параметры слоя(размер входа, выхода; гиперпараметры)
        self.f = Frame(root_widget, bd=1, relief=SUNKEN)

        # виджет-надпись отображает имя слоя
        self.lab = Label(self.f, bd=1, relief=RAISED, text=name_layer)

        # отслеживание движения
        self.lab.bind('<ButtonPress-1>', self.start_move_window)
        self.lab.bind('<B1-Motion>', self.move_window)
        self.f.bind('<ButtonPress-1>', self.start_move_window)
        self.f.bind('<B1-Motion>', self.move_window)

    def pack(self):
        """
        Располагает виджет. Полезно, потому что можно передавать координаты в
        этот метод из главного окна и друг за другом выстраивать слои
        """

        self.f.place(x=self.__winX, y=self.__winY, width=200, height=200)
        self.lab.pack(fill=X, padx=1, pady=1)

    def start_move_window(self, event):
        """
        Отлавливает момент фокуса мышки на виджете
        """

        self.__lastX = event.x_root
        self.__lastY = event.y_root

    def move_window(self, event):
        """
        Двигает виджет слоя(рамку и надпись)
        """

        self.root.update_idletasks()

        # использование координат главного окна для вычисления смещения для внутренних координат виджета
        self.__winX += event.x_root - self.__lastX
        self.__winY += event.y_root - self.__lastY

        # запоминаем последние координаты
        self.__lastX = event.x_root
        self.__lastY = event.y_root

        # запоминаем последние координаты
        self.f.place_configure(x=self.__winX, y=self.__winY)


class DataView(ttk.Frame):
    """
    Вкладка загрузки данных.
    """

    def __init__(self, container):
        super().__init__()
        pass
