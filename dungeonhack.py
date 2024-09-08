import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsView, QGraphicsScene
from dungeon_generator import DungeonGenerator  # Import DungeonGenerator class
from debugger import DebuggerWindow  # Import DebuggerWindow class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dungeonhack")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Create dungeon
        self.dungeon = DungeonGenerator(40, 20, 6)
        self.dungeon.generate_dungeon()

        # Draw initial dungeon
        DungeonGenerator.draw_dungeon(self.scene, list(self.dungeon.layers.values()))

        # Open debugger window
        self.open_debugger()

    def open_debugger(self):
        self.debugger_window = DebuggerWindow(self.dungeon, self.scene)
        self.debugger_window.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())