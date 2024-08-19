class BankAccount:
    def __init__(self, balance, acc_num):
        self.__balance = balance
        self.__acc_num = acc_num
    def deposit(self, dep):
        self.__balance += dep
    def withdraw(self, withd):
        if self.__balance >= withd:
            self.__balance -= withd
        else:
            print("Insufficient funds")
    def get_balance(self):
        return self.__balance
    def get_acc_num(self):
        return self.__acc_num
    def __iadd__(self, other):
        self.deposit(other)
        return self
    def __isub__(self, other):
        self.withdraw(other)
        return self
    def __str__(self):
        return f"Account Number: {self.__acc_num}\nBalance: {self.__balance}"
    
BankAccount_1 = BankAccount(1000,'1234567890')
BankAccount_1.deposit(500)
BankAccount_1.withdraw(1200)
print(BankAccount_1)