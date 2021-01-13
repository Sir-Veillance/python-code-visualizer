global_string = "This is a global string"
test_list = [1, 2, 3, 4, 5]
global_int = 612
formatted_string = f"Test {global_int * 2}"
a, b = 100, 200

# this is sample code for testing purposes with parsing and debugging implementation

# price class for both classes could be implemented in the __init__ method but for sample sake they are being
# implemented as separate methods to allow for more interesting parsing


class Bundle:
    def __init__(self, discount, *args):
        self.discount = discount
        self.items = args

    def __str__(self):
        s = f"Bundle ({self.discount}) {{"
        for item in self.items:
            for line in str(item).splitlines():
                s += f"\n  {line}"
        s += "\n}"
        return s

    def get_price(self):
        price = 0
        for item in self.items:
            price += item.get_price()
        return price * self.discount


class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return self.name + "\n"

    def get_price(self):
        return self.price


if 1 < 0 or 2 < 5:
    print("test")
    a = 5
    print("test2")


if __name__ == "__main__":
    item_one = Item("Item One", 15.00)
    item_two = Item("Item Two", 8.00)
    item_three = Item("Item Three", 13.00)
    bundle_one = Bundle(0.9, item_one, item_two, item_three)
    item_four = Item("Item Four", 10.00)
    bundle_two = Bundle(0.5, item_four, bundle_one)

    print(f"{bundle_two.get_price():.2f}")
    print(bundle_two)
