from typing import List


# класс для хранения информации об операциях
class Operation:
    # Типы операций храним в свойствах класса
    DEPOSIT = 'Пополнение'
    WITHDRAW = 'Снятие'
    TRANSFER_OUT = 'Перевод'
    TRANSFER_IN = 'Поступление'

    # Напоминаю: обращение к этим переменным происходит через имя класса, пример: Operation.WITHDRAW

    def __init__(self, type, amount, target_account=None):
        self.type = type
        self.amount = amount
        self.target_account = target_account

    def __repr__(self) -> str:
        """
        :return: возвращает строковое представление операции. Формат указан в 02_IBank_part2.md
        """
        str_out = f"{self.type} {self.amount} руб."
        if self.type == Operation.TRANSFER_OUT:
            str_out += f" на счет клиента: {self.target_account.name}"
        if self.type == Operation.TRANSFER_IN:
            str_out += f" со счета клиента: {self.target_account.name}"
        return str_out


class Account:
    def __init__(self, name: str, passport: str, phone_number: str, start_balance: int = 0):
        self.name = name
        self.passport = passport
        self.phone_number = phone_number
        # self.balance = start_balance
        self.__balance = start_balance
        # историю храним как список объектов класса Operation, добавив свойство в конструктор:
        self.__history: List[Operation] = []

    # Данный метод дан в готовом виде. Изучите его и используйте как пример, для доработки других
    def deposit(self, amount: int, to_history: bool = True) -> None:
        """
        Внесение суммы на текущий счет
        :param amount: сумма
        :param to_history: True - записывать операцию в историю, False - не записывать
        """
        self.__balance += amount
        if to_history:
            operation = Operation(amount, Operation.DEPOSIT)
            self.__history.append(operation)

    def full_info(self) -> str:
        """
        Полная информация о счете в формате: "Иван баланс: 100 руб. паспорт: 3200 123456 т.+7-900-200-02-03"
        """
        return f"{self.name} баланс: {self.balance} руб. паспорт: {self.passport} т.{self.phone_number}"

    def __repr__(self) -> str:
        """
        :return: Информацию о счете в виде строки в формате "Иван баланс: 100 руб."
        """
        return f"{self.name} баланс: {self.balance} руб."

    @property
    def balance(self) -> int:
        return self.__balance

    def withdraw(self, amount: int, to_history: bool = True) -> None:
        """
        Снятие суммы с текущего счета
        :param amount: сумма
        """
        if amount > self.balance:
            raise ValueError("Недостаточно средств")

        self.__balance -= amount
        if to_history:
            operation = Operation(amount, Operation.WITHDRAW)
            self.__history.append(operation)


    def transfer(self, target_account: 'Account', amount: int) -> None:
        """
        Перевод денег на счет другого клиента
        :param target_account: счет клиента для перевода
        :param amount: сумма перевода
        """
        self.withdraw(amount, to_history=False)
        target_account.deposit(amount, to_history=False)
        operation_my = Operation(Operation.TRANSFER_OUT, amount, target_account=target_account, )
        operation_target = Operation(Operation.TRANSFER_IN, amount, target_account=self)
        self.__history.append(operation_my)
        target_account.__history.append(operation_target)

    def get_history(self) -> List[Operation]:
        """
        :return: возвращаем историю операций в виде списка операций
        """
        return self.__history


if __name__ == "__main__":
    # Создаем тестовый аккаунт:
    account1 = Account("Иван", "3230 634563", "+7-900-765-12-34", 1000)
    account2 = Account("Алексей", "3232 456124", "+7-901-744-22-99", 200)

    # Выполняем пару операций пополнения:
    account1.transfer(account2, 800)
    # account1.deposit(200)
    # account1.deposit(500)

    # Выводим историю операций:
    print("account1 history")
    for operation in account1.get_history():
        print(operation)

    print("account2 history")
    for operation in account2.get_history():
        print(operation)
