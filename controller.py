from model import Model
from view import View
from view import DataView
from tkinter import filedialog as fd


class Controller:
    """
    Контроллер. Отслеживает нажатие кнопок на представлении
    """

    def __init__(self):
        self.model = Model()
        self.view = View(self)
        self.data_view = DataView(self)

    def print_layer(self, name_layer):
        """
        Только отрисовка слоя с именем
        """

        self.view.network_view.print_and_save_new_layer(name_layer)

    def add_layer(self, layer_meta_view):
        """
        Добавляет экземпляр представления слоя
        """

        self.model.add_layer(layer_meta_view)

    def delete_layer(self, layer):
        """
        :param layer: Представление слоя, которое нужно удалить
        Сначала по представлению(по его месту в памяти оно удаляется из списка слоев в модели, а потом на стороне view
        """
        self.model.delete_layer(layer)
        layer.destroy_widget()

    def save_model(self):
        self.model.save_model()

    # _____DATA_________________________________________________
    def get_datasets(self):
        return self.model.get_datasets()

    def set_dataset(self, dataset_name):
        self.model.set_dataset(dataset_name)

    def start_model(self):
        self.model.start()

    def main(self):
        self.view.main()  # отображаем главное окно


if __name__ == '__main__':
    controller = Controller()

    controller.main()
