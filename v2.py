from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# IMPORTS
from utils import Queue, Stack
import random
import time

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt" 
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# -- START CODE -- #
# -- START CODE -- #
t0 = time.time()
#### #### #### #### ####
##         V2...      ##
#### #### #### #### ####
# B) SETUP
visited_rooms = {}
backwards = {'n':'s', 'e':'w', 's':'n', 'w':'e'}

# C) HELPERS
def unused_exits(current_room, visited_rooms):
    ALL_room_exits = visited_rooms[current_room_ID]
    FILTREED_room_exits = []
    for direction in ALL_room_exits:
        if ALL_room_exits[direction] == '?' and current_room.get_room_in_direction(direction) not in visited_rooms:
            FILTREED_room_exits.append(direction)

    if FILTREED_room_exits:
        return FILTREED_room_exits
    else:
        return None

def choose_random_direction(unvisited_options):
    return unvisited_options[
        random.randint(0, len(unvisited_options) -1)
    ]


# D) STEPS 
# Create Stack
s = Stack()

while len(visited_rooms) < len(room_graph):
    # Add starting ROOM_ID to Stack => Starting point for DFS
    s.push(player.current_room.id)

    # Pop off stack
    current_room_ID = s.pop()
    current_room_OBJECT = world.rooms[current_room_ID]

    # check if current_room_id in visited_rooms
    if current_room_ID not in visited_rooms:
        visited_rooms[current_room_ID] = {}

        # Add mystery exits for current_rooms' AVAILABLE / VALID direction options
        for direction in current_room_OBJECT.get_exits():      # didnt use roomGraph just has the intergers not actual room objects w/ methods
            visited_rooms[current_room_ID][direction] = '?'

    # Find unused_exits
    DFS_unvisited_movement_options = unused_exits(current_room_OBJECT, visited_rooms)
    if DFS_unvisited_movement_options is not None:
        # Pick Random Direction
        chosen_direction = choose_random_direction(DFS_unvisited_movement_options)
        next_room = current_room_OBJECT.get_room_in_direction(chosen_direction).id
         
        # Update visited_rooms[current_room_ID][direction] w/ room id
        visited_rooms[current_room_ID][chosen_direction] = current_room_OBJECT.get_room_in_direction(chosen_direction).id

        # Move player in that direction
        player.travel(chosen_direction)

        # exit()
    else:
        pass



    
t1 = time.time()
total = t1 - t0
print(f'Total Time: {total}')
# -- END CODE -- #
# -- END CODE -- #


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
