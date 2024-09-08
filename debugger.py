from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QDialog, QGraphicsTextItem
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

from dungeon_generator import DungeonGenerator  # Import DungeonGenerator class
from layer import Layer
from layer_manager import LayerManager
from layer_widget import LayerWidget

DEBUG_MODE = True

# Function to draw the dungeon on the QGraphicsScene
def draw_dungeon(scene, layers):
    scene.clear()
    width = layers[0].width
    height = layers[0].height
    for y in range(height):
        for x in range(width):
            for layer in layers:
                if layer.visibility:
                    char = layer.data[y][x]
                    if char != ' ':
                        text_item = QGraphicsTextItem(char)
                        color = QColor(255, 255, 255, int(layer.transparency * 255))
                        text_item.setDefaultTextColor(color)
                        text_item.setFont(QFont("Courier", 10))
                        text_item.setPos(x * 10, y * 10)
                        scene.addItem(text_item)
                        break

# Debugger window class
class DebuggerWindow(QDialog):
    def __init__(self, dungeon, scene):
        super().__init__()
        self.setWindowTitle("Debugger")
        self.setGeometry(100, 100, 300, 600)
        self.setStyleSheet("color: white; background-color: black;")

        self.layout = QVBoxLayout(self)

        self.layers = [
            Layer('bg_white', 40, 20),
            Layer('bg_black', 40, 20),
            Layer('other_geo', 40, 20),
            Layer('walls', 40, 20),
            Layer('statics', 40, 20),
            Layer('player_sight', 40, 20),
            Layer('monster_sight', 40, 20),
            Layer('dynamic_lights', 40, 20),
            Layer('static_lights', 40, 20),
            Layer('entities', 40, 20)
        ]

        # Copy dungeon data to layers
        for layer in self.layers:
            layer.data = dungeon.layers[layer.name]

        self.layer_manager = LayerManager(self.layers)
        self.layout.addWidget(self.layer_manager)

        # Add LayerWidget instances to the layout
        for layer in self.layers:
            layer_widget = LayerWidget(layer)
            self.layout.addWidget(layer_widget)

# Main application window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dungeonhack")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.layout.addWidget(self.view)

        # Create dungeon
        self.dungeon = DungeonGenerator(40, 20, 6)
        self.dungeon.generate_dungeon()

        # Draw initial dungeon
        draw_dungeon(self.scene, list(self.dungeon.layers.values()))

        # Open debugger window
        self.open_debugger()

    def open_debugger(self):
        self.debugger_window = DebuggerWindow(self.dungeon, self.scene)
        self.debugger_window.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()