import random

# Constants for ASCII graphics
MONSTERS = ['.', 'O', 'x', 'X', '*']

class EncounterManager:
    def __init__(self):
        self.monsters = MONSTERS

    def trigger_random_encounter(self):
        return random.choice(self.monsters)