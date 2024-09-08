from PyQt5.QtWidgets import QVBoxLayout, QWidget
from layer_widget import LayerWidget

class LayerManager(QWidget):
    def __init__(self, layers):
        super().__init__()
        self.layers = layers
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.update_layers()

    def add_layer(self, layer):
        self.layers.append(layer)
        self.update_layers()

    def remove_layer(self, layer):
        self.layers.remove(layer)
        self.update_layers()

    def move_layer(self, from_index, to_index):
        layer = self.layers.pop(from_index)
        self.layers.insert(to_index, layer)
        self.update_layers()

    def update_layers(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        for layer in self.layers:
            layer_widget = LayerWidget(layer)
            self.layout.addWidget(layer_widget)