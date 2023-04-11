from layers import *


class Model:
    """
    Модель. Отвечает за данные и исполнение вычислительных процессов
    """

    def __init__(self):
        pass

    def create_layer(self, name_layer):
        layers_from_pytorch = {'relu': LayerReLU()}
        new_layer = layers_from_pytorch[name_layer]
        print(new_layer)
        return new_layer
