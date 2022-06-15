from board import Board
from match import Match
from player import Player
from random import randint
from queue import Queue
import eel
import threading

command_queue = Queue()
command_queue_recv = Queue()
player = None
color_map = [
    "blue",
    "red",
    "green",
    "yellow",
]
dice = 0

state = "roll" # waiting|play|roll

def main():
    board = Board("abc", [])
    
    player_1 = Player("Zhafran", 0)
    player_2 = Player("Ubay", 1)
    global player
    global dice
    player = player_1

    board.add_player(player_1)
    board.add_player(player_2)

    n = 0
    while True:
        i = command_queue.get()
        i = int(i)
        
        global state
        if state == "waiting":
            i = int(command_queue_recv.get())
        elif state == "play":
            if i == 5:
                board.player_troop_out(n)
            elif board.move_player_troop_possible(n, i, dice):
                board.move_player_troop(n, i, dice)
            else:
                print("Not possible")

            n += 1

            if n == 2:
                n = 0
        elif state == "roll":
            if i == 6:
                dice = randint(1, 6)
                print("Dice {}".format(dice))
                board.print_troops()
                print("Player {} got {} step".format(n, dice))

                if board.player_troops_at_base(n) == 4 and dice != 6:
                    print("Skipping")
                    state = "waiting"
                    continue
                state = "play"

def start():
    t = threading.Thread(target=main)
    t.start()

@eel.expose
def put_command(new_command):
    command_queue.put(new_command)

@eel.expose
def handle_click(element_id):
    print(element_id)
    if color_map[player.player_number] in element_id:
        eel.alert_func("yeay")

@eel.expose
def get_dice():
    global dice
    return dice

    
