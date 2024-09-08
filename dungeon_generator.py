from PyQt5.QtWidgets import QGraphicsTextItem
from PyQt5.QtGui import QFont, QColor

class Layer:
    def __init__(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height
        self.data = [[' ' for _ in range(width)] for _ in range(height)]
        self.visibility = True
        self.transparency = 1.0  # 1.0 is fully opaque, 0.0 is fully transparent
        self.mask = None  # Mask layer

    def set_transparency(self, value):
        self.transparency = value

    def set_visibility(self, visible):
        self.visibility = visible

    def set_mask(self, mask_layer):
        self.mask = mask_layer

class DungeonGenerator:
    def __init__(self, width, height, num_rooms):
        self.width = width
        self.height = height
        self.num_rooms = num_rooms
        self.layers = {
            'bg_white': Layer('bg_white', width, height),
            'bg_black': Layer('bg_black', width, height),
            'other_geo': Layer('other_geo', width, height),
            'walls': Layer('walls', width, height),
            'statics': Layer('statics', width, height),
            'player_sight': Layer('player_sight', width, height),
            'monster_sight': Layer('monster_sight', width, height),
            'dynamic_lights': Layer('dynamic_lights', width, height),
            'static_lights': Layer('static_lights', width, height),
            'entities': Layer('entities', width, height)
        }
        self.layer_order = ['bg_white', 'bg_black', 'other_geo', 'walls', 'statics', 'player_sight', 'monster_sight', 'dynamic_lights', 'static_lights', 'entities']
        self.layer_visibility = {layer: True for layer in self.layer_order}
        self.layer_transparency = {layer: 1.0 for layer in self.layer_order}

    def generate_dungeon(self):
        # Fill bg_white with solid white (space character)
        for y in range(self.height):
            for x in range(self.width):
                self.layers['bg_white'].data[y][x] = ' '

        # Fill bg_black with solid black (solid block character)
        for y in range(self.height):
            for x in range(self.width):
                self.layers['bg_black'].data[y][x] = '█'

        # Example: Add some other_geo elements
        for y in range(2, self.height - 2):
            self.layers['other_geo'].data[y][2] = 'O'
            self.layers['other_geo'].data[y][self.width - 3] = 'O'

        # Generate walls, statics, player_sight, monster_sight, dynamic_lights, static_lights, and entities here
        # Example: Add some walls
        for y in range(1, self.height - 1):
            self.layers['walls'].data[y][1] = '#'
            self.layers['walls'].data[y][self.width - 2] = '#'
        for x in range(1, self.width - 1):
            self.layers['walls'].data[1][x] = '#'
            self.layers['walls'].data[self.height - 2][x] = '#'

        # Example: Add some statics (e.g., treasure chests)
        self.layers['statics'].data[5][5] = 'C'  # C for chest

        # Example: Add some player sight (e.g., player vision range)
        self.layers['player_sight'].data[6][6] = 'P'  # P for player sight

        # Example: Add some monster sight (e.g., monster vision range)
        self.layers['monster_sight'].data[7][7] = 'M'  # M for monster sight

        # Example: Add some dynamic lights (e.g., moving light sources)
        self.layers['dynamic_lights'].data[8][8] = 'L'  # L for light

        # Example: Add some static lights (e.g., torches)
        self.layers['static_lights'].data[6][6] = 'T'  # T for torch

        # Example: Add some entities (e.g., player)
        self.layers['entities'].data[10][10] = '@'  # @ for player

    def toggle_layer_visibility(self, layer_name):
        if layer_name in self.layer_visibility:
            self.layer_visibility[layer_name] = not self.layer_visibility[layer_name]

    def toggle_layer_transparency(self, layer_name):
        if layer_name in self.layer_transparency:
            self.layer_transparency[layer_name] = not self.layer_transparency[layer_name]

    # Function to draw the dungeon on the QGraphicsScene
    @staticmethod
    def draw_dungeon(scene, layers):
        scene.clear()
        if not layers:
            return

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