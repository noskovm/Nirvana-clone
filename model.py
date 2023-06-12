import torch.nn as nn
import tqdm as tqdm
from torchvision.datasets import MNIST
from layers import *
from torch.utils.data import DataLoader
import torchvision
import torchvision.transforms as T
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import clear_output
from tqdm.notebook import tqdm


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

        # список доступных датасетов
        self.datasets = ['CIFAR10', 'MNIST']

        # строка-имя датасета
        self.choose_dataset_string = None

        # уникальный датасет из torchvision
        self.dataset = None

        # разделение выборки
        self.train_set = None
        self.test_set = None

        self.train_loader = None
        self.test_loader = None

        self.device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
        self.model = LeNet().to(self.device)
        self.optimizer = torch.optim.SGD(self.model.parameters(), lr=1e-2, momentum=0.9)
        self.scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(self.optimizer, T_max=100)
        self.criterion = nn.CrossEntropyLoss()


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
        self.choose_dataset_string = dataset_name
        self.dataset = getattr(torchvision.datasets, f'{dataset_name}')

        # сделать разделение выборки
        self.set_train_and_test_sets()
        return True

    def set_train_and_test_sets(self):
        # todo сделать анимацию загрузки
        transform = T.Compose([T.ToTensor(), T.Resize((32, 32))])
        self.train_set = self.dataset(f'{self.choose_dataset_string}', transform=transform, train=True, download=True)
        self.test_set = self.dataset(f'{self.choose_dataset_string}', transform=transform, train=False, download=True)
        self.train_loader = DataLoader(self.train_set, batch_size=64, shuffle=True)
        self.test_loader = DataLoader(self.test_set, batch_size=64, shuffle=False)
        return True

    def train(self):
        NUM_EPOCHS = 2
        train_losses, train_accuracies = [], []
        test_losses, test_accuracies = [], []

        for epoch in range(1, NUM_EPOCHS + 1):
            train_loss, train_accuracy = 0.0, 0.0
            self.model.train()
            for images, labels in self.train_loader:
                images = images.to(self.device)
                labels = labels.to(self.device)

                self.optimizer.zero_grad()
                # images: batch_size x num_channels x height x width
                logits = self.model(images)
                # logits: batch_size x num_classes
                loss = self.criterion(logits, labels)
                loss.backward()
                self.optimizer.step()

                train_loss += loss.item() * images.shape[0]
                train_accuracy += (logits.argmax(dim=1) == labels).sum().item()

            if self.scheduler is not None:
                self.scheduler.step()

            train_loss /= len(self.train_loader.dataset)
            train_accuracy /= len(self.train_loader.dataset)
            train_losses += [train_loss]
            train_accuracies += [train_accuracy]

            test_loss, test_accuracy = 0.0, 0.0
            self.model.eval()
            for images, labels in self.test_loader:
                images = images.to(self.device)
                labels = labels.to(self.device)

                with torch.no_grad():
                    logits = self.model(images)
                    # logits: batch_size x num_classes
                    loss = self.criterion(logits, labels)

                test_loss += loss.item() * images.shape[0]
                test_accuracy += (logits.argmax(dim=1) == labels).sum().item()

            test_loss /= len(self.test_loader.dataset)
            test_accuracy /= len(self.test_loader.dataset)
            test_losses += [test_loss]
            test_accuracies += [test_accuracy]
            self.plot_losses(train_losses, test_losses, train_accuracies, test_accuracies)

    def plot_losses(self, train_losses, test_losses, train_accuracies, test_accuracies):
        clear_output()
        fig, axs = plt.subplots(1, 2, figsize=(13, 4))
        axs[0].plot(range(1, len(train_losses) + 1), train_losses, label='train')
        axs[0].plot(range(1, len(test_losses) + 1), test_losses, label='test')
        axs[0].set_ylabel('loss')

        axs[1].plot(range(1, len(train_accuracies) + 1), train_accuracies, label='train')
        axs[1].plot(range(1, len(test_accuracies) + 1), test_accuracies, label='test')
        axs[1].set_ylabel('accuracy')

        for ax in axs:
            ax.set_xlabel('epoch')
            ax.legend()

        plt.show()

    def start(self):
        self.train()


class LeNet(nn.Module):
    def __init__(self, image_channels=1):
        super().__init__()
        self.encoder = nn.Sequential(  # 32 x 32
             nn.Conv2d(in_channels=image_channels, out_channels=6, kernel_size=5),  # 28 x 28
             nn.Tanh(),
             nn.AvgPool2d(2),  # 14 x 14
             nn.Conv2d(in_channels=6, out_channels=16, kernel_size=5),  # 10 x 10
             nn.Tanh(),
             nn.AvgPool2d(2),  # 5 x 5
             nn.Conv2d(in_channels=16, out_channels=120, kernel_size=5)  # 1 x 1
        )
        self.model = Model()
        self.encoder = self.model.neural_network

        self.head = nn.Sequential(
            nn.Linear(in_features=120, out_features=84),
            nn.Tanh(),
            nn.Linear(in_features=84, out_features=10)
        )

    def forward(self, x):
        # x: B x 1 x 32 x 32
        out = self.encoder(x)
        # out: B x 120 x 1 x 1
        out = out.squeeze(-1).squeeze(-1)
        # out: B x 120
        out = self.head(out)
        # out: B x 10
        return out


