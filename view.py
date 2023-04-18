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
        self._make_add_conv2d_button()

        # установка фрейма для слоев
        self.layers_frame = ttk.Frame(self, height=200, width=200)
        self.layers_frame.pack(anchor=N, padx=20, pady=100)

        # сетка для слоев
        self.row = 0
        self.col = 0
        self.layers_frame.rowconfigure(index=self.row, weight=1)
        self.layers_frame.columnconfigure(index=self.col, weight=1)

        # установка нижнего фрейма для кнопки сохранения модели
        self.save_model_button_frame = ttk.Frame(self, height=60, padding=[8, 8], border=1, relief=RAISED)
        self.save_model_button_frame.pack(anchor=S, fill=X, expand=True)
        self.save_model_button_frame.pack_propagate(False)

        # отрисовка кнопки сохранения
        self._make_save_model_button()

    def print_and_save_new_layer(self, name_layer):
        """
        Здесь сохраняем представление слоя в модели, чтобы потом можно было брать метаинфу(параметры, например)
        """

        new_layer = LayerWidgetView(master=self.layers_frame, name_layer=str(name_layer))

        self.controller.add_layer(new_layer)    # благодаря этому можно передавать в torch параметры слоя

        new_layer.pack_widget(col=self.col)  # слой помещается в текущий столбец
        self.col += 1  # теперь столбцов нужно больше
        self.layers_frame.columnconfigure(index=self.col, weight=1)  # переопределяем количество столбцов

    def _make_add_linear_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='Linear',
                                   command=lambda: self.controller.print_layer('linear'))
        linear_button.pack(side=LEFT)

    def _make_add_relu_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='ReLU',
                                   command=lambda: self.controller.print_layer('relu'))
        linear_button.pack(side=LEFT, padx=5)

    def _make_add_conv2d_button(self):
        conv2d_button = ttk.Button(self.layers_buttons_frame, text='Conv2d',
                                   command=lambda: self.controller.print_layer('Conv2d'))
        conv2d_button.pack(side=LEFT, padx=5)

    def _make_save_model_button(self):
        save_model_button = ttk.Button(self.save_model_button_frame, text='SAVE',
                                       command=self.controller.save_model)
        save_model_button.pack(anchor=E)

    # todo для каждой кнопки
    # сделать функцию отрисовки make
    # в layer_widget сделать _make_features
    # в layer_widget сделать get_all_parameters
    # в model прописать в словарь
    # в layers написать функцию

    # todo решить проблему с непропорциональностью отображения параметров в слое



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
        # понадобится для определения какие параметры слоя показывать
        self.name_layer = name_layer

        # главная рамка
        self.main_layer_frame = ttk.Frame(master, width=150, height=235)

        # все параметры и кнопки(внутрення рамка, все кнопки кроме параметров in_features и out_features)
        self.inner_layer_frame = ttk.Frame(self.main_layer_frame, relief=RAISED, border=1, width=150, height=170)

        # фрейм для отрисовки параметров конкретного слоя
        self.outer_layer_frame = ttk.Frame(self.main_layer_frame, width=150, height=170)

        # виджет-надпись отображает имя слоя
        self.text_layer = ttk.Label(self.inner_layer_frame, relief=RAISED, text=name_layer, background='gray90')

    def _make_layers_features(self):
        """
        У каждого слоя свой набор редактируемых параметров, например у линейного это in_features, out_features.
        Эта функция сопоставляет какие параметры нужно отрисовать исходя из имени слоя
        """

        match self.name_layer:
            case 'linear':

                # создаем сетку 4x4(так просто красивее выглядит) для размещения двух параметров в фрейме
                for row in range(4):
                    for col in range(4):
                        self.outer_layer_frame.rowconfigure(index=row, weight=1)
                        self.outer_layer_frame.columnconfigure(index=col, weight=1)

                # in_features, out_features labels
                self.text_in_features = ttk.Label(self.outer_layer_frame, text='IN')
                self.text_out_features = ttk.Label(self.outer_layer_frame, text='OUT')

                # in_features, out_features entries
                self.in_features_entry = ttk.Entry(self.outer_layer_frame, width=4)
                self.out_features_entry = ttk.Entry(self.outer_layer_frame, width=4)

                # param labels pack
                self.text_in_features.grid(row=0, column=0, sticky=W, pady=1)
                self.text_out_features.grid(row=1, column=0, sticky=W, pady=1)

                # param entries pack
                self.in_features_entry.grid(row=0, column=1, sticky=W, pady=1)
                self.out_features_entry.grid(row=1, column=1, sticky=W, pady=1)

            case 'Conv2d':

                for row in range(6):
                    for col in range(4):
                        self.outer_layer_frame.rowconfigure(index=row, weight=1)
                        self.outer_layer_frame.columnconfigure(index=col, weight=1)

                # in_features, out_features labels
                self.text_in_channels = ttk.Label(self.outer_layer_frame, text='IN')
                self.text_out_channels = ttk.Label(self.outer_layer_frame, text='OUT')
                self.text_kernel_size = ttk.Label(self.outer_layer_frame, text='kernel size')
                self.text_stride = ttk.Label(self.outer_layer_frame, text='stride')

                # in_features, out_features entries
                self.in_channels_entry = ttk.Entry(self.outer_layer_frame, width=4)
                self.out_channels_entry = ttk.Entry(self.outer_layer_frame, width=4)
                self.kernel_size_entry = ttk.Entry(self.outer_layer_frame, width=4)
                self.stride_entry = ttk.Entry(self.outer_layer_frame, width=4)

                # param labels pack
                self.text_in_channels.grid(row=0, column=0, sticky=W, pady=1)
                self.text_out_channels.grid(row=1, column=0, sticky=W, pady=1)
                self.text_kernel_size.grid(row=2, column=0, sticky=W, pady=1)
                self.text_stride.grid(row=3, column=0, sticky=W, pady=1)

                # param entries pack
                self.in_channels_entry.grid(row=0, column=1, sticky=W, pady=1)
                self.out_channels_entry.grid(row=1, column=1, sticky=W, pady=1)
                self.kernel_size_entry.grid(row=2, column=1, sticky=W, pady=1)
                self.stride_entry.grid(row=3, column=1, sticky=W, pady=1)
    def pack_widget(self, col):
        """
        Располагает виджет слоя в сетке слоев
        """

        # упаковка фреймов
        self.main_layer_frame.grid(row=0, column=col, padx=20)
        self.main_layer_frame.pack_propagate(False)
        self.inner_layer_frame.pack(fill=X, pady=5)
        self.inner_layer_frame.pack_propagate(False)
        self.outer_layer_frame.pack(fill=X)
        self.outer_layer_frame.pack_propagate(False)

        # inner pack
        self.text_layer.pack(fill=X, padx=1, pady=1)

        # outer pack
        self._make_layers_features()

    def get_all_parameters(self, name_layer):
        match name_layer:
            case 'linear':
                parameters = dict()
                parameters['in_features'] = int(self.in_features_entry.get())
                parameters['out_features'] = int(self.out_features_entry.get())
                return parameters

            case 'relu':
                return None

