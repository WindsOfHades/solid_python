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

    def pay(self, payment_type, security_code):
        if payment_type == "debit":
            print("processing debit payment ...")
            print(f"verify security code: {security_code}")
            self._status = "paid"
        elif payment_type == "credit":
            print("processing debit payment ...")
            print(f"verify security code: {security_code}")
            self._status = "paid"
        else:
            raise Exception(f"Wrong payment type: {payment_type}")

    def __repr__(self) -> str:
        msg = "----- Order -----\n"
        msg += f"items: {self._items}\n"
        msg += f"quantities: {self._quantities}\n"
        msg += f"price: {self._prices}\n"
        msg += f"status: {self._status}\n"
        msg += "-----------------\n"
        return msg


def main():
    order_phone = Order()
    order_car = Order()
    order_phone.add_item("Samsung", 1, 10000)
    order_car.add_item("Volvo", 1, 500000)
    print(order_phone)
    print(order_car)
    print(order_phone)


if __name__ == "__main__":
    main()
