"""
The problem appears if you have too generic interfaces that not every class can use.

For example if the Payment interface adds a functionality for 2Factor authentication by SMS.
Every client (e.g. PaymentCreditCard) needs to implement (or raise exeption for that generic functionality).
Let's say only Paypal and Debit needs this type of authentication.


Interface segragation principle offers:
Break the interfaces into more lego peice interfaces that different
client classes can pick and choose.
This way the classes with special needs that do not want the other functionality are
not forced to implement unnecessary methods or raise exeception for them.

So in this example we either:
define a separate interface (with payment as super) e.g. SmsAuthenticator.
or:
use composition to have authenticator type in different sub classes

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


# This is interface segragation via inheretance
# class can choose what interaface they implement now
# commented out as composition way makes more sense here
# class SmsAuthenticator(Payment):
#     @abstractmethod
#     def authenticate(self, sms_code) -> None:
#         pass


class SmsAuth:
    def __init__(self) -> None:
        self._authorized = False

    @property
    def authorized(self) -> bool:
        return self._authorized

    def verify_sms_code(self, code) -> None:
        print(f"Verifying the code: {code}")
        self._authorized = True


class PaymentDebitCard(Payment):
    def __init__(self, security_code: str, authorizer: SmsAuth):
        self._security_code: str = security_code
        self._authorizer: SmsAuth = authorizer

    def pay(self, order: Order) -> None:
        if not self._authorizer.authorized:
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
    def __init__(self, email_address: str, authorizer: SmsAuth):
        self._email_address: str = email_address
        self._authorizer: SmsAuth = authorizer

    def pay(self, order: Order) -> None:
        if not self._authorizer.authorized:
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
    PaymentPaypal("alice@daemonico.com", sms_auth).pay(order_chair)
    print(order_phone)
    print(order_chair)
    print(order_car)


if __name__ == "__main__":
    main()
