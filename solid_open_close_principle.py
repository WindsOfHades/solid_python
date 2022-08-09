"""
If we need to support more payment types, now we need to
change the `Payment` class (imagine it was in another file resting in peace)
These changes could be adding more functions, if statements, more arguments, ...

Open-Close principle says once you wrote a class you should hardly need to
modify the exisiting code. (Open for extension and Close for modification)

To acheive that you can add new classes (typically implementing an interface or abstract class)
That does specific functionality for each requirement (instead of modifying the old class and adding if/else).

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
        msg += f"status: {self._status}\n"
        msg += "-----------------\n"
        return msg


class Payment(ABC):
    @abstractmethod
    def pay(self, order: Order, security_code: str) -> None:
        pass


class PaymentDebitCard(Payment):
    def pay(self, order: Order, security_code: str) -> None:
        print("Processing debit payment ...")
        print(f"verify security code: {security_code}")
        order.status = "paid"


class PaymentCreditCard(Payment):
    def pay(self, order: Order, security_code: str) -> None:
        print("Processing a credit check ...")
        print(f"verify security code: {security_code}")
        order.status = "paid"


class PaymentPaypal(Payment):
    def pay(self, order: Order, security_code: str) -> None:
        print("Signing in to paypal service ...")
        # The following line breaks Liskov's principle since
        # this child object expects email address but receives
        # email address, so some dirty hack needs to be done that
        # changes the expected behaviour and from now on these
        # objects cannot be interchanged with each other without breaking
        # the code
        print(f"verify email address: {security_code}")
        order.status = "paid"


def main():
    order_phone = Order()
    order_car = Order()
    order_chair = Order()
    order_phone.add_item("Samsung", 1, 10000)
    order_car.add_item("Volvo", 1, 500000)
    order_chair.add_item("office", 2, 5000)
    PaymentDebitCard().pay(order_phone, "1234")
    PaymentPaypal().pay(order_chair, "1234")
    print(order_phone)
    print(order_chair)
    print(order_car)


if __name__ == "__main__":
    main()
