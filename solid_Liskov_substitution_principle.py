"""
The Liskov principle says that objects of a superclass shall be replaceable with objects of its subclasses
without breaking the application i.e. you shall not dirty hack your subclass so that it won't
break the functionality you receive from the parent class.

1. Don't implement any stricter validation rules on input parameters than implemented by
the parent class (should be the same or less).

2. The return value of a method of the subclass needs to comply with the same rules as the return value
of the method of the superclass. (at least the same or more)

If you follow the above different kind of objects could be used interchangably but still won't break
the code.

Moral of the story: model your classes based on behaviours not on properties;
model your data based on properties and not on behaviours.

Take a look at the PaymentPaypal, since this type of payment does not need
the card's security code. It needs to hack that extra argument so that it can
still work even though one has changed the behaviour of the parent (but forced to from the parent)

One way to fix this is to use the security code outside of pay() method and accept it
in the constructor.

The other way would be to use composition instead of inheritence.

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


class PaymentDebitCard(Payment):
    def __init__(self, security_code: str):
        self._security_code: str = security_code

    def pay(self, order: Order) -> None:
        print("Processing debit payment ...")
        print(f"verify security code: {self._security_code}")
        order.status = "paid"


class PaymentCreditCard(Payment):
    def __init__(self, security_code: str):
        self._security_code: str = security_code

    def pay_credit(self, order: Order) -> None:
        print("Processing a credit check ...")
        print(f"verify security code: {self._security_code}")
        order.status = "paid"


class PaymentPaypal(Payment):
    def __init__(self, email_address: str):
        self._email_address: str = email_address

    def pay(self, order: Order) -> None:
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
    PaymentDebitCard("1234").pay(order_phone)
    PaymentPaypal("alice@daemonico.com").pay(order_chair)
    print(order_phone)
    print(order_chair)
    print(order_car)


if __name__ == "__main__":
    main()
