from layers import *


class Model:
    """
    Модель. Отвечает за данные и исполнение вычислительных процессов
    """

    def __init__(self):
        """
        layers_list хранит в себе представления слоев
        """

        self.layers_list = []
        self.layers_sequence = LayersSequence()
        self.layers_link = {'linear': LayerLinear}

    def add_layer(self, name_layer):
        """
        :param name_layer: имя слоя, ключ, по которому можно достать соотвествующий слой из pytorch
        :return: экземпляр класса pytorch name_layer
        """
        # словарь соответсвия между name_layer и таким же слоем из pytorch
        self.layers_list.append(name_layer)

    def save_model(self):
        """
        Проходится по каждому слою из представления, забирает все параметры и формирует torch.sequence
        """

        for layer in self.layers_list:
            current_parameters = layer.get_all_parameters(layer.name_layer)
            for name_param, value_param in current_parameters.items():
                print(name_param, value_param)
