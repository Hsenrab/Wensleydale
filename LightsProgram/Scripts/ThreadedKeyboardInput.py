import threading, time
from msvcrt import getch

key = "lol"


def thread1():
    global key
    lock = threading.Lock()
    while True:
        with lock:
            key = getch()


threading.Thread(target=thread1).start()

while True:
    time.sleep(10)
    print(key)