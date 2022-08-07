"""
Now Order has single responsibility
Payment has single responisibily

This increased the cohision
But still introduced coupling between the classes
"""


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


class Payment:
    def pay_debit(self, order: Order, security_code: str):
        print("processing debit payment ...")
        print(f"verify security code: {security_code}")
        order.status = "paid"

    def pay_credit(self, order: Order, security_code: str):
        print("processing debit payment ...")
        print(f"verify security code: {security_code}")
        order.status = "paid"


def main():
    order_phone = Order()
    order_car = Order()
    order_phone.add_item("Samsung", 1, 10000)
    order_car.add_item("Volvo", 1, 500000)
    print(order_phone)
    Payment().pay_debit(order_phone, "1234")
    print(order_car)
    print(order_phone)


if __name__ == "__main__":
    main()
