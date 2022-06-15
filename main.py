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

state = "roll" # waiting|play|roll
state_lock = threading.Lock()

def main():
    board = Board("abc", [])
    
    player_1 = Player("Zhafran", 0)
    player_2 = Player("Ubay", 1)
    global player
    global dice
    global state
    player = player_1

    board.add_player(player_1)
    board.add_player(player_2)

    n = 0
    while True:
        if state == "play":
            i = command_queue.get()
            i = int(i)
        print("acquiring at main")
        state_lock.acquire()
        print("state", state)
        if state == "waiting":
            state_lock.release()
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
            state_lock.release()
        elif state == "roll":
            x = command_queue_recv.get()
            print(x)
            print(str(type(x)))
            x = x["data"]["action"]
            dice = x.replace("dice_", "")
            print("Dice {}".format(dice))
            board.print_troops()
            print("Player {} got {} step".format(n, dice))

            if board.player_troops_at_base(n) == 4 and dice != 6:
                print("Skipping")
                state = "waiting"
                continue
            else:
                state = "play"
            state_lock.release()

server_address=('45.118.135.250', 8888)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    # logging.warning(f"connecting to {server_address}")
    try:
        # logging.warning(f"sending message ")
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
        return hasil
    except Exception as e:
        print(e)
        logging.warning("error during data receiving")
        return False

def pull_message():
    while True:
        res = send_command("ask")
        print(res)
        try:
            if res["status"] == "OK":
                command_queue_recv.put(res["data"])
        except:
            pass
        time.sleep(10)

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
    print(element_id)
    if color_map[player.player_number] in element_id:
        eel.alert_func("yeay")

@eel.expose
def get_dice():
    global dice
    return dice

    
