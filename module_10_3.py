import threading
from threading import Thread, Lock
import random
import time


class Bank(threading.Thread):
    def __init__(self, balance=0, lock=Lock):
        super().__init__()
        self.balance = balance
        self.lock = lock()
    def deposit(self):
        for i in range(100):
            a = random.randint(50, 500) #увеличение баланса
            if self.balance >= 500 and self.lock.locked():
                self.lock.release()
            self.balance += a
            print(f'Пополнение: {a}. Баланс: {self.balance}')
            time.sleep(0.01)

    def take(self):
        for i in range(100):
            b = random.randint(50, 500) #уменьшение баланса
            print(f'Запрос на {b}')
            if b <= self.balance:
                self.balance -= b
                print(f'Снятие: {b}. Баланс: {self.balance}.')
            else:
                print(f'Запрос отклонён, недостаточно средств')
                self.lock.acquire()

bk = Bank()

th1 = Thread(target=Bank.deposit, args=(bk,)) # Т.к. методы принимают self, в потоки нужно передать сам объект класса Bank
th2 = Thread(target=Bank.take, args=(bk,))

th1.start()
th2.start()
th1.join()
th2.join()

print(f'Итоговый баланс: {bk.balance}')


