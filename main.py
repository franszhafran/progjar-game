from board import Board
from match import Match
from player import Player
from random import randint
from queue import Queue
import eel
import threading
import time
import socket
import logging
import json

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

state = "waiting" # waiting|play|roll
state_lock = threading.Lock()
gameplay_data = []
players = []

def main():
    board = Board("abc", [])
    
    player_1 = Player("Zhafran", 0)
    player_2 = Player("Ubay", 1)
    players.append(player_1)
    players.append(player_2)
    global player
    global dice
    global state

    board.add_player(player_1)
    board.add_player(player_2)

    n = 0
    last_dice = 0
    while True:
        try:
            print("Player number", player.player_number)
            n = player.player_number
            color = color_map[n]
        except Exception as e:
            continue
        print("acquiring state at main")
        print("Gameplay data")
        print(gameplay_data)
        state_lock.acquire()
        print("state", state)
        if state == "play":
            state_lock.release()
            i = command_queue.get()
            i = int(i)
            if i == 6:
                continue
            print("got on play", n, i, last_dice)
            if i == 5:
                board.player_troop_out(n)
                func_name = "start{}1".format(color)
                bar = getattr(eel, func_name)
                result = bar()
                send_command("troopout_{}_{}".format(n, 3))
            else:
                print("test")
                board.move_player_troop(n, i, last_dice)
                steps = board.players[n].last_steps_index
                player = board.players[n]
                movement = player.process_steps_to_movement(steps)
                troop_id = "{}-1".format(color)
                print("dd")
                eel.move_troop(troop_id, movement)
                print("aa")
                send_command("troopmove_{}_{}_{}".format(n, 3, last_dice))
                print("gg")
            state_lock.acquire()
            state = "waiting"
            state_lock.release()
        elif state == "waiting":
            state_lock.release()
            x = command_queue_recv.get()
            state_lock.acquire()
            print("Got from cmd queue rcv", x)
            print(x)
            try:
                data = x["data"]
                for e in data:
                    action = e["action"]
                    print("Gameplay data append with a {}".format(action))
                    gameplay_data.append(action)
                    
                    if "continue" in action:
                        continue
                    data = action.split("_")

                    if "troopout" in action:
                        player_number = int(data[1])
                        troop_number = int(data[2])
                        board.player_troop_out(player_number)
                        func_name = "start{}1".format(color_map[player_number])
                        bar = getattr(eel, func_name)
                        result = bar()
                    elif "troopmove" in action:
                        if int(data[1]) != player.player_number:
                            player_number = int(data[1])
                            troop_number = int(data[2])
                            steps = int(data[3])
                            board.move_player_troop(player_number, troop_number, steps)
                            func_name = "{}-1".format(color_map[player_number])
                            steps = board.players[player_number].last_steps_index
                            player = board.players[player_number]
                            movement = player.process_steps_to_movement(steps)
                            eel.move_troop(func_name, movement)
                            state = "waiting"
                    elif "dice" in action:
                        print("Printing dice data", int(data[1]), player.player_number)

                        if int(data[1]) != player.player_number:
                            print("Not our action, skipping")
                            continue

                        dice = int(data[2])
                        last_dice = dice
                        print("Dice {}".format(dice))
                        board.print_troops()
                        print("Player {} got {} step".format(n, dice))

                        if board.player_troops_at_base(n) == 4 and dice != 6:
                            print("Skipping")
                            state = "waiting"
                            send_command("continue_" + str(player.player_number))
                            break
                        else:
                            state = "play"
                        print("state now", state)
                state_lock.release()
            except Exception as e:
                raise            
        elif state == "roll":
            print("state:", state)

server_address=('45.118.135.250', 8888)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    # logging.warning(f"connecting to {server_address}")
    try:
        print("sending message::bottom")
        print(command_str)
        command_str += "\r\n\r\n"
        sock.sendall(command_str.encode())
        # Look for the response, waiting until socket is done (no more data)
        data_received="" #empty string
        while True:
            #socket does not receive all data at once, data comes in part, need to be concatenated at the end of process
            data = sock.recv(16)
            if data:
                #data is not empty, concat with previous content
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                # no more data, stop the process by break
                break
        # at this point, data_received (string) will contain all data coming from the socket
        # to be able to use the data_received as a dict, need to load it using json.loads()
        data_received = data_received.replace("\r\n", "")
        hasil = json.loads(data_received)
        command_queue_recv.put(hasil)
        # logging.warning("data received from server:")
        sock.close()
        print("response from::{} {}".format(command_str, str(hasil)))
        return hasil
    except Exception as e:
        print(e)
        logging.warning("error during data receiving")
        return False

def pull_message():
    while True:
        res = send_command("ask")
        try:
            if res["status"] == "OK":
                if len(res["data"]) > 0:
                    pass
                else:
                    global player
                    if player is None:
                        player = players[int(res["player_number"])]
        except:
            pass
        time.sleep(3)

def start():
    t = threading.Thread(target=main)
    t.start()

    t2 = threading.Thread(target=pull_message)
    t2.start()

@eel.expose
def put_command(new_command):
    command_queue.put(new_command)

@eel.expose
def handle_click(element_id):
    if color_map[player.player_number] in element_id:
        command_queue.put(5)

@eel.expose
def get_dice():
    global dice
    return dice

@eel.expose
def move(element_id):
    command_queue.put(3)

    
