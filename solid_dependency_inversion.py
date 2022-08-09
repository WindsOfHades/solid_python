"""

Dependency inversion says:

Make classes dependent on interfaces or Abstract classes rather than concrete objects.
This way you can pass in different types that all implement that behaviour without
changing the existing code. So you will decouple the objects from each other.

Just like Liskov's substitution principle, DIP promotes usage of abstractions.
The only difference is that LSP focuses on:
Correcteness of the behaviour and following the contract when switching different sub types.

DIP focuses on:
Decoupling objects so that they can easily be switched.

In the example below let's say we have a separate kind of authorizer, preferably
your classes shall be decoupled enough so that they can use a different authorization method.

"""


from abc import ABC, abstractmethod


class Order:
    def __init__(self) -> None:
        self._items = []
        self._quantities = []
        self._prices = []
        self._status = "open"

    def add_item(self, name, quantity, price):
        self._items.append(name)
        self._quantities.append(quantity)
        self._prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self._prices)):
            total += self._quantities[i] * self._prices[i]
        return total

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status) -> None:
        self._status = status

    def __repr__(self) -> str:
        msg = "----- Order -----\n"
        msg += f"items: {self._items}\n"
        msg += f"quantities: {self._quantities}\n"
        msg += f"price: {self._prices}\n"
        msg += f"Total price: {self.total_price()}\n"
        msg += f"status: {self._status}\n"
        msg += "-----------------\n"
        return msg


class Payment(ABC):
    @abstractmethod
    def pay(self, order: Order) -> None:
        pass


class Authorizer(ABC):
    @abstractmethod
    def is_authorized(self) -> bool:
        pass


class SmsAuth(Authorizer):
    def __init__(self) -> None:
        self._authorized = False

    def is_authorized(self) -> bool:
        return self._authorized

    def verify_sms_code(self, code) -> None:
        print(f"Verifying the SMS code: {code}")
        self._authorized = True


class RobotAuth(Authorizer):
    def __init__(self) -> None:
        self._authorized = False

    def is_authorized(self):
        return self._authorized

    def verify_not_robot(self) -> None:
        print("processing that you are not a robot...")
        self._authorized = True


class PaymentDebitCard(Payment):
    def __init__(self, security_code: str, authorizer: Authorizer):
        self._security_code: str = security_code
        self._authorizer: SmsAuth = authorizer

    def pay(self, order: Order) -> None:
        if not self._authorizer.is_authorized():
            raise Exception("Authorization failed")
        print("Processing debit payment ...")
        print(f"verify security code: {self._security_code}")
        order.status = "paid"


class PaymentCreditCard(Payment):
    def __init__(self, security_code: str):
        self._security_code: str = security_code

    def pay(self, order: Order) -> None:
        print("Processing a credit check ...")
        print(f"verify security code: {self._security_code}")
        order.status = "paid"


class PaymentPaypal(Payment):
    def __init__(self, email_address: str, authorizer: Authorizer):
        self._email_address: str = email_address
        self._authorizer: Authorizer = authorizer

    def pay(self, order: Order) -> None:
        if not self._authorizer.is_authorized():
            raise Exception("Authorization failed")
        print("Signing in to paypal service ...")
        print(f"verify email address: {self._email_address}")
        order.status = "paid"


def main():
    order_phone = Order()
    order_car = Order()
    order_chair = Order()
    order_phone.add_item("Samsung", 1, 10000)
    order_car.add_item("Volvo", 1, 500000)
    order_chair.add_item("office", 2, 5000)
    sms_auth = SmsAuth()
    sms_auth.verify_sms_code("1234")
    PaymentDebitCard("1234", sms_auth).pay(order_phone)
    robot_auth = RobotAuth()
    robot_auth.verify_not_robot()
    PaymentPaypal("alice@daemonico.com", robot_auth).pay(order_chair)
    print(order_phone)
    print(order_chair)
    print(order_car)


if __name__ == "__main__":
    main()
