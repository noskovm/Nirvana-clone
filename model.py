from layers import *


class Model:
    """
    Модель. Отвечает за данные и исполнение вычислительных процессов
    """

    def __init__(self):
        """
        layers_list на этапе формирования каркаса сети(без параметров) мы должны только запоминать
            последовательность слоев
        """

        self.layers_list = []




    def add_layer(self, name_layer):
        """
        :param name_layer: имя слоя, ключ, по которому можно достать соотвествующий слой из pytorch
        :return: экземпляр класса pytorch name_layer
        """
        # словарь соответсвия между name_layer и таким же слоем из pytorch
        self.layers_list.append(name_layer)
        print(self.layers_list)
