import json
import random

# Function to generate a random map
def generate_map(width, height):
    """
    Generates a map of given width and height filled with empty spaces.
    
    Args:
    width (int): The width of the map.
    height (int): The height of the map.
    
    Returns:
    list: A 2D list representing the map.
    """
    return [[' ' for _ in range(width)] for _ in range(height)]

# Function to check if a room can be placed at the given position
def can_place_room(map, top_left_x, top_left_y, room_width, room_height, min_distance=2):
    """
    Checks if a room can be placed at the given position without overlapping other rooms.
    
    Args:
    map (list): The map where rooms are being placed.
    top_left_x (int): The x-coordinate of the top-left corner of the room.
    top_left_y (int): The y-coordinate of the top-left corner of the room.
    room_width (int): The width of the room.
    room_height (int): The height of the room.
    min_distance (int): The minimum distance required from other rooms.
    
    Returns:
    bool: True if the room can be placed, False otherwise.
    """
    for i in range(-min_distance, room_height + min_distance):
        for j in range(-min_distance, room_width + min_distance):
            if 0 <= top_left_y + i < len(map) and 0 <= top_left_x + j < len(map[0]):
                if map[top_left_y + i][top_left_x + j] == '#':
                    return False
    return True

# Define a struct for the rooms
class Room:
    def __init__(self, top_left_x, top_left_y, width, height):
        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.width = width
        self.height = height
        self.inventory = []
        self.is_secret = False
        self.is_safe = True  # Set is_safe to True by default
        self.is_exit = False
        self.is_entrance = False

# Function to add random rooms to the map
def add_random_rooms(map):
    """
    Adds random rooms to the map until at least 50% of the map is filled with rooms.
    Ensures that at least 90% of the rooms are at least 2 squares away from the nearest room.
    
    Args:
    map (list): The map where rooms are being placed.
    """
    height = len(map)
    width = len(map[0])
    total_tiles = width * height
    filled_tiles = 0
    max_attempts = 1000  # Maximum number of attempts to place a room
    attempts = 0 
    square_rooms = 0
    rooms_placed = 0
    rooms_with_distance = 0
    rooms = []
    
    while filled_tiles < total_tiles // 2 and attempts < max_attempts:
        if square_rooms < 4 or random.random() < 0.5:
            room_width = random.randint(4, min(width, height) // 2)  # Ensure room width is at least 4
            room_height = (room_width * 3) // 4  # Ensure room height is 3/4 of the width
            square_rooms += 1
        else:
            room_width = random.randint(2, min(width, height) // 2)  # Ensure room width is at least 2
            room_height = random.randint(2, min(width, height) // 2)  # Ensure room height is at least 2

        # Add padding of 1 to all sides of the room
        padded_room_width = room_width + 2
        padded_room_height = room_height + 2

        top_left_x = random.randint(1, width - padded_room_width - 1)
        top_left_y = random.randint(1, height - padded_room_height - 1)

        if can_place_room(map, top_left_x, top_left_y, padded_room_width, padded_room_height):
            for i in range(padded_room_height):
                for j in range(padded_room_width):
                    map[top_left_y + i][top_left_x + j] = '#'
                    filled_tiles += 1
            rooms_placed += 1
            if can_place_room(map, top_left_x, top_left_y, padded_room_width, padded_room_height, min_distance=2):
                rooms_with_distance += 1

            room = Room(top_left_x, top_left_y, padded_room_width, padded_room_height)
            rooms.append(room)

            prev_top_left_x = top_left_x
            prev_top_left_y = top_left_y
            prev_padded_room_width = padded_room_width
            prev_padded_room_height = padded_room_height

        attempts += 1

    if rooms_placed > 0 and rooms_with_distance / rooms_placed < 0.9:
        print("Warning: Less than 90% of the rooms are at least 2 squares away from the nearest room.")

    return rooms

# Function to calculate the distance between two rooms
def calculate_distance(room1, room2):
    """
    Calculates the Manhattan distance between two rooms.
    
    Args:
    room1 (Room): The first room.
    room2 (Room): The second room.
    
    Returns:
    int: The Manhattan distance between the two rooms.
    """
    room1_center_x = room1.top_left_x + room1.width // 2
    room1_center_y = room1.top_left_y + room1.height // 2
    room2_center_x = room2.top_left_x + room2.width // 2
    room2_center_y = room2.top_left_y + room2.height // 2
    return abs(room1_center_x - room2_center_x) + abs(room1_center_y - room2_center_y)

# Function to connect rooms with hallways
def connect_rooms(map, rooms):
    """
    Connects rooms with hallways.
    
    Args:
    map (list): The map where rooms are being placed.
    rooms (list): The list of rooms to be connected.
    """
    for i in range(len(rooms) - 1):
        room1 = rooms[i]
        room2 = rooms[i + 1]

        # Get the perimeter points of the rooms
        room1_perimeter_x = room1.top_left_x + room1.width // 2
        room1_perimeter_y = room1.top_left_y + room1.height // 2
        room2_perimeter_x = room2.top_left_x + room2.width // 2
        room2_perimeter_y = room2.top_left_y + room2.height // 2

        # Adjust the perimeter points to be at the edge of the rooms
        if room1_perimeter_x < room2.top_left_x:
            room1_perimeter_x = room1.top_left_x + room1.width - 1
        elif room1_perimeter_x > room2.top_left_x + room2.width:
            room1_perimeter_x = room1.top_left_x

        if room1_perimeter_y < room2.top_left_y:
            room1_perimeter_y = room1.top_left_y + room1.height - 1
        elif room1_perimeter_y > room2.top_left_y + room2.height:
            room1_perimeter_y = room1.top_left_y

        if room2_perimeter_x < room1.top_left_x:
            room2_perimeter_x = room2.top_left_x + room2.width - 1
        elif room2_perimeter_x > room1.top_left_x + room1.width:
            room2_perimeter_x = room2.top_left_x

        if room2_perimeter_y < room1.top_left_y:
            room2_perimeter_y = room2.top_left_y + room2.height - 1
        elif room2_perimeter_y > room1.top_left_y + room1.height:
            room2_perimeter_y = room2.top_left_y

        # Create horizontal hallway
        if room1_perimeter_x != room2_perimeter_x:
            for x in range(min(room1_perimeter_x, room2_perimeter_x), max(room1_perimeter_x, room2_perimeter_x) + 1):
                map[room1_perimeter_y - 1][x] = '#'
                map[room1_perimeter_y][x] = '#'
                map[room1_perimeter_y + 1][x] = '#'

        # Create vertical hallway
        if room1_perimeter_y != room2_perimeter_y:
            for y in range(min(room1_perimeter_y, room2_perimeter_y), max(room1_perimeter_y, room2_perimeter_y) + 1):
                map[y][room2_perimeter_x - 1] = '#'
                map[y][room2_perimeter_x] = '#'
                map[y][room2_perimeter_x + 1] = '#'

# Function to create a black mask with white outlines
def create_mask(map):
    """
    Creates a black mask with white outlines of the map.
    
    Args:
    map (list): The map to create a mask for.
    
    Returns:
    list: The mask with white outlines.
    """
    mask = [[' ' for _ in range(len(map[0]))] for _ in range(len(map))]
    for y in range(1, len(map) - 1):
        for x in range(1, len(map[0]) - 1):
            if map[y][x] == '#':
                if (map[y-1][x] == ' ' or map[y+1][x] == ' ' or
                    map[y][x-1] == ' ' or map[y][x+1] == ' '):
                    mask[y][x] = '#'
    return mask

# Main function to generate and print the map and mask
def main():
    """
    Main function to generate a map with random rooms, print it, and create a mask.
    """
    width = 80
    height = 25
    
    map = generate_map(width, height)
    rooms = add_random_rooms(map)
    connect_rooms(map, rooms)
    
    for row in map:
        print(''.join(row))

    mask = create_mask(map)
    print("\nMask:\n")
    for row in mask:
        print(''.join(row))

    # Print room details
    for room in rooms:
        print(f"Room at ({room.top_left_x}, {room.top_left_y}) with size {room.width}x{room.height}")
        print(f"Inventory: {room.inventory}")
        print(f"Is Secret: {room.is_secret}, Is Safe: {room.is_safe}, Is Exit: {room.is_exit}, Is Entrance: {room.is_entrance}")

    # Save the dungeon to a JSON file
    dungeon_data = {
        "map": map,
        "rooms": [
            {
                "top_left_x": room.top_left_x,
                "top_left_y": room.top_left_y,
                "width": room.width,
                "height": room.height,
                "inventory": room.inventory,
                "is_secret": room.is_secret,
                "is_safe": room.is_safe,
                "is_exit": room.is_exit,
                "is_entrance": room.is_entrance
            }
            for room in rooms
        ]
    }

    with open("saved_dungeon.json", "w") as json_file:
        json.dump(dungeon_data, json_file, indent=4)

if __name__ == "__main__":
    main()

# Generated by Copilot