from datetime import datetime
from sys import stderr
from threading import Thread
from time import sleep

from functions.functions import account_initial_setup
from functions.schedules import create_scheduler
from functions.streamings import htl_listen, login, ltl_listen

if __name__ == "__main__":
    client = login()
    account_initial_setup(client)
    ltl_thread = Thread(target=ltl_listen, args=(client,), daemon=True)
    htl_thread = Thread(target=htl_listen, args=(client,), daemon=True)
    ltl_thread.start()
    htl_thread.start()
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
