import sv_ttk
from tkinter import *
from tkinter import ttk


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
        self.geometry('1820x980')
        self.state('zoomed')

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

        self.data_view = DataView(master=self.tub, controller=self.controller)
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

    def __init__(self, controller, master=None):
        super().__init__()
        self.controller = controller

        # установка верхнего фрейма для кнопок-слоев
        self.layers_buttons_frame = ttk.Frame(self, height=100, padding=[8, 15], border=1, relief=RAISED)
        self.layers_buttons_frame.pack(anchor=NW)
        self._make_grid_for_top_buttons_frame()

        # отрисовка кнопок-слоев в верхнем фрейме
        self._make_add_linear_button()
        self._make_add_relu_button()
        self._make_add_conv2d_button()

        # установка фрейма для слоев
        self.layers_frame = ttk.Frame(self, height=200)
        self.layers_frame.pack(anchor=N, padx=20, pady=200)

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

        new_layer = LayerWidgetView(master=self.layers_frame, name_layer=str(name_layer), controller=self.controller)

        self.controller.add_layer(new_layer)  # благодаря этому можно передавать в torch параметры слоя

        new_layer.pack_widget(col=self.col)  # слой помещается в текущий столбец
        self.col += 1  # теперь столбцов нужно больше
        self.layers_frame.columnconfigure(index=self.col, weight=1)  # переопределяем количество столбцов

    def _make_grid_for_top_buttons_frame(self):
        for row in range(2):
            for col in range(6):
                self.layers_buttons_frame.rowconfigure(index=row, weight=1)
                self.layers_buttons_frame.columnconfigure(index=col, weight=1)

    def _make_add_linear_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='Linear',
                                   command=lambda: self.controller.print_layer('Linear'))
        linear_button.grid(row=0, column=0, padx=5, pady=3)

    def _make_add_relu_button(self):
        linear_button = ttk.Button(self.layers_buttons_frame, text='ReLU',
                                   command=lambda: self.controller.print_layer('ReLU'))
        linear_button.grid(row=0, column=1, padx=5, pady=3)

    def _make_add_conv2d_button(self):
        conv2d_button = ttk.Button(self.layers_buttons_frame, text='Conv2d',
                                   command=lambda: self.controller.print_layer('Conv2d'))
        conv2d_button.grid(row=0, column=2, padx=5, pady=3)
        # todo доделать сонв по всем параметрам

    def _make_save_model_button(self):
        save_model_button = ttk.Button(self.save_model_button_frame, text='SAVE',
                                       command=self.controller.save_model)
        save_model_button.pack(anchor=E)

    # todo для каждой кнопки
    # сделать функцию отрисовки make !
    # в layer_widget сделать _make_features
    # в layer_widget сделать get_all_parameters
    # в model прописать в словарь
    # в layers написать функцию

    # todo решить проблему с непропорциональностью отображения параметров в слое


class DataView(ttk.Frame):
    """
    Вкладка загрузки данных.
    """

    def __init__(self, controller, master=None):
        super().__init__(master)
        self.controller = controller
        self.add_file_button = ttk.Button(text='+', command=self.controller.add_data)
        self.add_file_button.pack()


class HyperView(ttk.Frame):
    """
    Вкладка подбора гиперпараметров.
    """

    def __init__(self, master=None):
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

    def __init__(self, master, name_layer, controller):
        super().__init__()
        # понадобится для определения какие параметры слоя показывать
        self.name_layer = name_layer
        self.controller = controller

        # главная рамка
        self.main_layer_frame = ttk.Frame(master, width=150, height=260)

        # все параметры и кнопки(внутрення рамка, все кнопки кроме параметров in_features и out_features)
        self.inner_layer_frame = ttk.Frame(self.main_layer_frame, height=170, border=1, relief=RAISED)

        # фрейм для отрисовки параметров конкретного слоя
        self.outer_layer_frame = ttk.Frame(self.main_layer_frame, height=170)

        # фрейм для надписи и кнопки удаления
        self.label_frame = Frame(self.inner_layer_frame, height=30, background='gray90')

        # виджет-надпись отображает имя слоя
        self.text_layer = ttk.Label(self.label_frame, relief=RAISED, text=name_layer, justify=LEFT, background='gray90',
                                    padding=[5, 0, 0, 0])

        # кнопка для удаления слоя
        self.delete_button_icon = PhotoImage(file='./icons/delete.png')
        self.delete_button = Button(self.label_frame, width=30, image=self.delete_button_icon, padx=10,
                                    borderwidth=0, background='gray90',
                                    command=lambda: self.controller.delete_layer(self))

    def _make_layers_features(self):
        """
        У каждого слоя свой набор редактируемых параметров, например у линейного это in_features, out_features.
        Эта функция сопоставляет какие параметры нужно отрисовать исходя из имени слоя
        """

        match self.name_layer:
            case 'Linear':

                # создаем сетку 4x4(так просто красивее выглядит) для размещения двух параметров в фрейме
                for row in range(6):
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

                # in_features, out_features labels
                self.text_in_channels = ttk.Label(self.outer_layer_frame, text='in_channels', foreground='gray',
                                                  font='Segoe 10')
                self.text_out_channels = ttk.Label(self.outer_layer_frame, text='out_channels', foreground='gray',
                                                   font='Segoe 10')
                self.text_kernel_size = ttk.Label(self.outer_layer_frame, text='kernel_size', foreground='gray',
                                                  font='Segoe 10')
                self.text_stride = ttk.Label(self.outer_layer_frame, text='stride', foreground='gray',
                                             font='Segoe 10')

                # in_features, out_features entries
                self.in_channels_entry = ttk.Entry(self.outer_layer_frame, width=4)
                self.out_channels_entry = ttk.Entry(self.outer_layer_frame, width=4)
                self.kernel_size_entry = ttk.Entry(self.outer_layer_frame, width=4)
                self.stride_entry = ttk.Entry(self.outer_layer_frame, width=4)

                # param labels pack
                self.text_in_channels.pack(side=TOP, anchor=NW)
                self.in_channels_entry.pack(side=TOP, anchor=NW, pady=(2, 5))

                self.text_out_channels.pack(side=TOP, anchor=NW)
                self.out_channels_entry.pack(side=TOP, anchor=NW, pady=(2, 5))

                self.text_kernel_size.pack(side=TOP, anchor=NW)
                self.kernel_size_entry.pack(side=TOP, anchor=NW, pady=(2, 5))

                self.text_stride.pack(side=TOP, anchor=NW)
                self.stride_entry.pack(side=TOP, anchor=NW, pady=(2, 0))
                # param entries pack

    def pack_widget(self, col):
        """
        Располагает виджет слоя в сетке слоев
        """

        # упаковка фреймов
        self.main_layer_frame.grid(row=0, column=col, padx=20)
        self.main_layer_frame.pack_propagate(False)
        self.inner_layer_frame.pack(fill=X)
        self.inner_layer_frame.pack_propagate(False)
        self.outer_layer_frame.pack(fill=BOTH, pady=5)
        # self.outer_layer_frame.pack_propagate(False)

        # inner pack
        self.label_frame.pack(fill=X)
        self.label_frame.pack_propagate(False)
        self.text_layer.pack(side=LEFT, fill=BOTH)
        self.delete_button.pack(side=RIGHT, fill=Y)

        # outer pack
        self._make_layers_features()

    def get_all_parameters(self, name_layer):
        """
        :param name_layer: по имени слоя передает необходимой словарь параметров
        :return: словарь параметров для слоя
        """
        match name_layer:
            case 'Linear':
                parameters = dict()
                parameters['in_features'] = int(self.in_features_entry.get())
                parameters['out_features'] = int(self.out_features_entry.get())
                return parameters

            case 'ReLU':
                return None

    def destroy_widget(self):
        """
        Удаляет self из представления
        :return:
        """
        self.main_layer_frame.destroy()
