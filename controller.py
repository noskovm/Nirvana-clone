from model import Model
from view import View
from tkinter import filedialog as fd


class Controller:
    """
    Контроллер. Отслеживает нажатие кнопок на представлении
    """

    def __init__(self):
        self.model = Model()
        self.view = View(self)

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
    def add_data(self):
        filetypes = (
            ('All files', '*.*')
        )

        path = fd.askopenfilename(
            title='Open a file',
            initialdir='/')

        if path != "":
            self.model.save_data(path)

    def main(self):
        self.view.main()  # отображаем главное окно


if __name__ == '__main__':
    controller = Controller()

    controller.main()
