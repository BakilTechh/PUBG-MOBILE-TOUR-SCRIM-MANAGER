class Item:
    total_item = 0
    __base_price = 10

    def __init__(self, name: str, price: int):
        if price <= 0:
            price = 10
        self.name = name
        self.__price = price * Item.__base_price
        Item.total_item += 1

    def __str__(self):
        return f"Nama: {self.name}\nHarga: {self.__price}"

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, value: int):
        self.__price = max(0, self.__price + value)

    @classmethod
    def base_price(cls, value):
        cls.__base_price = max(0, cls.__base_price + value)


class ItemStack:
    def __init__(self, item: Item, stack: int):
        self.item = item
        self.__stack = stack

    def __str__(self):
        return f"{self.item.__str__()}\nTumpukan: {self.__stack}"

    @property
    def stack(self):
        return self.__stack

    @stack.setter
    def stack(self, value: int):
        self.__stack = max(0, self.__stack + value)


class Inventory:
    max_slot = 10

    def __init__(self):
        self.__slot = Inventory.max_slot
        self.list_item = []

    def add_item(self, item: ItemStack):
        if item in self.list_item:
            pos = self.list_item.index(item)
            self.list_item[pos].stack += item.stack
        elif len(self.list_item) < self.__slot:
            self.list_item.append(item)
        else:
            print("Maaf, Inventaris Penuh")

    def delete_item_from_inventory(self):
        self.list_item = [i for i in self.list_item if i.stack > 0]

    def show_list_item(self):
        for i in self.list_item:
            print(i)


class Character:
    def __init__(self, name):
        if not self.name_validation(name):
            raise ValueError("Nama tidak boleh mengandung angka")
        self.name = name
        self.__gold = 0
        self.inventory = Inventory()

    @property
    def gold(self):
        return self.__gold

    @gold.setter
    def gold(self, value):
        self.__gold = max(0, self.__gold + value)

    @staticmethod
    def name_validation(name: str):
        return isinstance(name, str) and name.isalpha()


if __name__ == "__main__":
    print("UJI CLASS METHOD ")
    Item.base_price(15)
    print("Class method berhasil dipanggil")

    print("\nUJI OBJEK ")
    item1 = Item("Cangkul Besi", 2)
    item2 = Item("Potion Merah", 1)

    stack1 = ItemStack(item1, 1)
    stack2 = ItemStack(item2, 5)

    player1 = Character("Arthur")
    player2 = Character("Merlin")

    print("\nUJI INSTANCE METHOD ")
    print("Inventaris Sebelum:\n")
    player1.inventory.show_list_item()

    player1.inventory.add_item(stack1)
    player1.inventory.add_item(stack2)
    print("Inventaris Sesudah:")
    player1.inventory.show_list_item()
    print()

    player1.inventory.add_item(stack2)
    print("Inventaris Sesudah Ditambah Lagi:")
    player1.inventory.show_list_item()
    print()

    print("\nUJI SETTER ")
    player1.gold = 100
    stack1.stack = 5
    print(f"Emas {player1.name} (Valid): {player1.gold}")
    print(f"Cangkul Besi (Valid): {stack1.stack}")

    player1.gold = -500
    stack1.stack = -10
    print(f"Emas {player1.name} (Tidak Valid -500): {player1.gold} (Tertahan di 0)")
    print(f"Tumpukan Pedang (Tidak Valid -10): {stack1.stack} (Tertahan di 0)")

    print("\nUJI HAPUS ITEM (INSTANCE METHOD) ")
    print("Inventaris Sebelum Dihapus:\n")
    player1.inventory.show_list_item()

    player1.inventory.delete_item_from_inventory()

    print("\nInventaris Sesudah Dihapus:")
    player1.inventory.show_list_item()

    print("\nUJI STATIC METHOD")
    uji_nama = Character.name_validation("Lancelot")
    print(f"Hasil static method untuk 'Lancelot': {uji_nama}")

    print("Uji coba membuat karakter dengan angka (akbar123)...")
    try:
        player_error = Character("akbar123")
    except ValueError as e:
        print(f"Error tertangkap: {e}")