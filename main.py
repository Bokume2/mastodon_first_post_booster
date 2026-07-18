from datetime import datetime
from sys import stderr
from threading import Thread
from time import sleep

from functions.schedules import create_scheduler
from functions.streamings import listen, login

if __name__ == "__main__":
    client = login()
    thread = Thread(target=listen, args=(client,), daemon=True)
    thread.start()
    print("start listening timeline")

    scheduler = create_scheduler(client)
    print("start schedule preparation")
    while True:
        try:
            scheduler.run_pending()
            sleep(5)
        except Exception as e:
            print(datetime.now(), file=stderr)
            print(e, file=stderr)
            print(file=stderr)
