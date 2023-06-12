import torch.nn as nn
from torchvision.datasets import MNIST
from layers import *
from torch.utils.data import DataLoader


class Model:
    """
    Модель. Отвечает за данные и исполнение вычислительных процессов
    """

    def __init__(self):
        """
        layers_list хранит в себе представления слоев
        """
        self.data = None
        self.layers_list = []
        self.neural_network = nn.Sequential()
        self.layers_link = {'Linear': make_linear_layer,
                            'ReLU': make_relu_layer}
        self.datasets = ['CIFAR10', 'MNIST']
        # self.MNIST = getattr(torchvision.datasets, 'MNIST')
        #
        # self.dataset_hmap = {'MNIST': self.MNIST}
        self.choose_dataset = None

    def add_layer(self, name_layer):
        """
        :param name_layer: имя слоя, ключ, по которому можно достать соотвествующий слой из pytorch
        :return: экземпляр класса pytorch name_layer
        """
        # словарь соответсвия между name_layer и таким же слоем из pytorch
        self.layers_list.append(name_layer)
        print(f'сейчас находятся {self.layers_list}')

    def save_model(self):
        """
        Проходится по каждому слою из представления, забирает все параметры и формирует torch.sequence
        """
        self.neural_network = nn.Sequential()  # при каждом нажатии на сохранение он заново все просчитывает

        for layer in self.layers_list:

            # словарь параметров для инициализации слоя
            current_parameters = layer.get_all_parameters(layer.name_layer)

            # с помощью имени знаем какую функцию вызывать для создания слоя
            name_layer = layer.name_layer

            if current_parameters:
                new_layer = self.layers_link[name_layer](current_parameters)
                self.neural_network.append(new_layer)
            else:
                new_layer = self.layers_link[name_layer]()
                self.neural_network.append(new_layer)

        for name, param in self.neural_network.named_parameters():
            print(name, param.shape)

    def delete_layer(self, layer):
        self.layers_list.remove(layer)

    def get_datasets(self):
        return self.datasets

    def set_dataset(self, dataset_name):
        self.choose_dataset = dataset_name
        print(f'Выбран датасет - {self.MNIST}')
        return True


