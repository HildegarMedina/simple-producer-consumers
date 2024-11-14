import random
from queue import Queue
import time
from concurrent.futures import ThreadPoolExecutor

menu = [
    {
        "name": "Pizza",
        "time_to_prepare": 10
    },
    {
        "name": "Spaghetti",
        "time_to_prepare": 5
    },
    {
        "name": "Burger",
        "time_to_prepare": 3
    },
    {
        "name": "Coke",
        "time_to_prepare": 2
    },
    {
        "name": "Ice Cream",
        "time_to_prepare": 2
    },
]

class Client: # PRODUCER
    def __init__(self, name):
        self.name = name
    
    def make_order(self, order, queue):
        time.sleep(2)
        print(f'================= MAKE ORDER ===================')
        print(f"{self.name} ordered {order['name']} and takes {order['time_to_prepare']} seconds to cook.")
        print('==================================================\n')
        queue.put(order)

class Cooker: # CONSUMERS
    def __init__(self, name):
        self.name = name
        self.busy = False

    def prepare_order(self, queue):
        while True:
            order = queue.get()
            if order is None:
                queue.task_done()
                break
            if order and self.busy == False:
                self.busy = True
                time.sleep(order['time_to_prepare'])
                print(f'================= PREPARED ORDER ================')
                print(f"{self.name} has prepared {order['name']}.")
                print('==================================================\n')
                self.busy = False
            queue.task_done()

if __name__ == "__main__":
    print('\n')

    queue = Queue()
    clients = [Client("Alice"), Client("Bob"), Client("Charlie"), Client("David"), Client("Evelin")]

    anakin_cooker = Cooker("Anakin")
    padme_cooker = Cooker("Padme")

    def make_order(queue):
        for client in clients:
            order = random.choice(menu)
            client.make_order(order, queue)
        queue.put(None)
        queue.put(None)

    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(make_order, queue)
        executor.submit(anakin_cooker.prepare_order, queue)
        executor.submit(padme_cooker.prepare_order, queue)

    queue.join()

    print('All works completed!!!')
