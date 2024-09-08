from PyQt5.QtWidgets import QFrame, QVBoxLayout, QCheckBox, QSlider, QLabel
from PyQt5.QtCore import Qt

class LayerWidget(QFrame):
    def __init__(self, layer):
        super().__init__()
        self.layer = layer
        self.setStyleSheet("color: white; background-color: black;")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.checkbox_visibility = QCheckBox(f"Show {layer.name}")
        self.checkbox_visibility.setChecked(layer.visibility)
        self.checkbox_visibility.stateChanged.connect(self.toggle_visibility)
        self.layout.addWidget(self.checkbox_visibility)

        self.slider_transparency = QSlider(Qt.Horizontal)
        self.slider_transparency.setValue(int(layer.transparency * 100))
        self.slider_transparency.valueChanged.connect(self.change_transparency)
        self.layout.addWidget(QLabel("Transparency"))
        self.layout.addWidget(self.slider_transparency)

    def toggle_visibility(self):
        self.layer.set_visibility(self.checkbox_visibility.isChecked())

    def change_transparency(self):
        self.layer.set_transparency(self.slider_transparency.value() / 100.0)