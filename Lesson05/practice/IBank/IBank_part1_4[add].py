import re

class Account:
    def __init__(self, name: str, passport: str, phone_number: str, start_balance: int = 0):
        Account.validate_passport_phone(passport, phone_number)
        self.name = name
        self.passport = passport
        self.phone_number = phone_number
        # self.balance = start_balance
        self.__balance = start_balance  # DONE: Закрываем прямой доступ к балансу

    def full_info(self) -> str:
        """
        Полная информация о счете в формате: "Иван баланс: 100 руб. паспорт: 3200 123456 т.+7-900-200-02-03"
        """
        return f"{self.name} баланс: {self.__balance} руб. паспорт: {self.passport} т.{self.phone_number}"

    def __repr__(self) -> str:
        """
        :return: Информацию о счете в виде строки в формате "Иван баланс: 100 руб."
        """
        return f"{self.name} баланс: {self.__balance} руб."

    # DONE: реализуйте getter для просмотра баланса
    #  Подробнее тут: https://pythobyte.com/using-getters-and-setters-in-python-5205-840ed13f/
    @property
    def balance(self) -> int:
        return self.__balance

    @balance.getter
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, new_balance) -> None:
        if new_balance <= 0 or not isinstance(new_balance, int): #type(new_cost) != int:
            raise ValueError("Balance must be greater than zero and integer")
        self.__balance += new_balance

    def deposit(self, amount: int) -> None:
        """
        Внесение суммы на текущий счет
        :param amount: сумма
        """
        self.__balance += amount

    # @balance.setter
    def withdraw(self, amount: int) -> None:
        """
        Снятие суммы с текущего счета
        :param amount: сумма
        """
        Account.check_balance(self.__balance, amount)
        self.__balance -= amount

    @staticmethod
    def validate_passport_phone(passport, phone_number):
        pattern = r"\d{4} \d{6}"
        if not re.match(pattern, passport):
            raise ValueError(f"Неверный формат паспорта")

        pattern_phone = r"[+]7-\d{3}-\d{3}-\d{2}-\d{2}"
        if not re.match(pattern_phone, phone_number):
            raise ValueError(f"Неверный формат телефона")

    @staticmethod
    def check_balance(balance, amount):
        if balance - amount < 0:
            raise ValueError(f"Недостаточно средств: {balance - amount}")

    # DONE-1: напишите реализацию метода transfer()
    def transfer(self, target_account: 'Account', amount: int) -> None:
        """
        Перевод денег на счет другого клиента
        :param target_account: счет клиента для перевода
        :param amount: сумма перевода
        :return:
        """
        Account.validate_passport_phone(self.passport, self.phone_number)
        target_account.validate_passport_phone(target_account.passport, target_account.phone_number)
        Account.check_balance(self.__balance, amount)
        self.withdraw(amount)
        target_account.deposit(amount)

    # DONE-1: добавьте проверку паспорта и телефона(в конструкторе) на соответствие заданным форматам
    #  В случае несоответствия выбрасываем исключение ValueError("Неверный формат телефона/паспорта")
    #  Проверка информации на корректность - валидация
    #  Готовые валидаторы можете взять в директории helpers


if __name__ == "__main__":
    # account1 = Account("Иван", "3230 634563", "+7-900-765-12-34", 1000)  # аккаунт с корректными данными
    # account2 = Account("Алексей", "323 456124", "+7-901-744-22-99")  # номер паспорта задан неверно
    # account3 = Account("Петр", "3232 456124", "+7-904-745-47", 400)  # номер телефона задан неверно
    try:
        account1 = Account("Иван", "3230 634563", "+7-900-765-12-34", 1000)
    except ValueError as e:
        print(e)
    try:
        account2 = Account("Алексей", "323 456124", "+7-901-744-22-99")  # номер паспорта задан неверно
    except ValueError as e:
        print(e)
    try:
        account3 = Account("Петр", "3232 456124", "+7-904-745-47", 400)  # номер телефона задан неверно
    except ValueError as e:
        print(e)
