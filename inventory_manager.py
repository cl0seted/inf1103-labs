from abc import ABC, abstractmethod
import json
from typing import Optional


# ------------------------------------------------------------
# Utility functions
# ------------------------------------------------------------

def printHeader() -> None:
    print(f"{'ID':<7} | {'Name':<20} | {'Price':<10} | {'Quantity':<8} | Supplier")


def pause_program() -> None:
    input("Press enter to continue:")


def stockInput() -> int:
    while True:
        try:
            stock = int(input("Enter stock quantity: "))
            if stock < 0:
                print("Stock cannot be negative!")
                continue
            return stock
        except ValueError:
            print("Stock must be a valid integer!")


def priceInput() -> float:
    while True:
        try:
            price = float(input("Enter product price: "))
            if price < 0:
                print("Price cannot be negative!")
                continue
            return price
        except ValueError:
            print("Your price must be a valid number!")


def sizeInput(product_type: str) -> float | int:
    while True:
        if product_type == "physical":
            try:
                size = float(input("Enter product weight in kilograms: "))
                if size <= 0:
                    print("Weight must be greater than zero.")
                    continue
                return size
            except ValueError:
                print("Please input a valid weight.")
        else:
            try:
                size = int(input("Enter product filesize in megabytes: "))
                if size <= 0:
                    print("Filesize must be greater than zero.")
                    continue
                return size
            except ValueError:
                print("Please input a valid integer.")


def get_valid_input() -> tuple[str, str, float, int, float | int, str, str]:
    match input("Enter product type: [P]hysical [D]igital\nChoice: ").lower():
        case "p":
            product_type = "physical"
        case "d":
            product_type = "digital"
        case _:
            print("Defaulting to product type: Physical")
            product_type = "physical"

    name = input("Enter product name: ").strip()
    size = sizeInput(product_type)
    price = priceInput()
    stock = stockInput()
    supplier_name = input("Enter supplier name: ").strip() or "Unknown Supplier"
    supplier_email = input("Enter supplier contact email: ").strip() or "Not provided"
    return name, product_type, price, stock, size, supplier_name, supplier_email


def appendType(item: "Product") -> str:
    return item.__class__.__name__.lower().replace("product", "")


# ------------------------------------------------------------
# Association: Supplier and Product
# A Supplier can exist independently of any Product.
# Product stores a reference to its Supplier.
# ------------------------------------------------------------

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> str:
        return (
            f"Supplier ID: {self.supplier_id} | "
            f"Name: {self.name} | Email: {self.contact_email}"
        )

    def to_dict(self) -> dict:
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_email": self.contact_email,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Supplier":
        return cls(
            supplier_id=data.get("supplier_id", "S0000"),
            name=data.get("name", "Unknown Supplier"),
            contact_email=data.get("contact_email", "Not provided"),
        )


# ------------------------------------------------------------
# Product hierarchy: inheritance, abstraction and polymorphism
# ------------------------------------------------------------

class Product(ABC):
    def __init__(
        self, prodID: str, name: str, price: float, stock: int, supplier: Supplier
    ):
        self.prodID: str = prodID
        self.name: str = name
        self.price: float = price
        self.stock: int = stock
        self.supplier: Supplier = supplier

    def update_stock(self, quantity: int) -> None:
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative.")
        print(f"Updating quantity of {self.name}")
        self.stock = quantity
        print("Product updated")

    def to_dict(self) -> dict:
        return {
            "prodID": self.prodID,
            "type": appendType(self),
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "supplier": self.supplier.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Product":
        product_type = data["type"]
        # The fallback allows inventory files created before Lab 8 to load.
        supplier_data = data.get(
            "supplier",
            {
                "supplier_id": "S0000",
                "name": "Unknown Supplier",
                "contact_email": "Not provided",
            },
        )
        supplier = Supplier.from_dict(supplier_data)

        if product_type == "physical":
            return PhysicalProduct.from_dict(data, supplier)
        if product_type == "digital":
            return DigitalProduct.from_dict(data, supplier)
        raise ValueError(f"Unknown product type: {product_type}")

    @abstractmethod
    def display_information(self) -> None:
        pass

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(
        self, prodID: str, name: str, price: float, stock: int,
        weight: float, supplier: Supplier
    ):
        super().__init__(prodID, name, price, stock, supplier)
        self.weight: float = weight

    def display_information(self) -> None:
        product_info = (
            f"{self.prodID:<7} | {self.name:<20} | "
            f"${self.price:<9.2f} | {self.stock:<8} | {self.supplier.name}"
            f" | Weight: {self.weight} kg"
        )
        print(product_info)

    @classmethod
    def from_dict(cls, data: dict, supplier: Optional[Supplier] = None) -> "PhysicalProduct":
        if supplier is None:
            supplier = Supplier.from_dict(data.get("supplier", {}))
        return cls(
            prodID=data["prodID"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            weight=data["weight"],
            supplier=supplier,
        )

    def get_fulfilment_info(self) -> str:
        return "I am a product that must be shipped"

    def calculate_shipping_cost(self) -> float:
        return round(self.weight * 0.7, 2)

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["weight"] = self.weight
        return data


class DigitalProduct(Product):
    def __init__(
        self, prodID: str, name: str, price: float, stock: int,
        download_size: int, supplier: Supplier
    ):
        super().__init__(prodID, name, price, stock, supplier)
        self.download_size: int = download_size

    def display_information(self) -> None:
        product_info = (
            f"{self.prodID:<7} | {self.name:<20} | "
            f"${self.price:<9.2f} | {self.stock:<8} | {self.supplier.name}"
            f" | Filesize: {self.download_size} MB"
        )
        print(product_info)

    @classmethod
    def from_dict(cls, data: dict, supplier: Optional[Supplier] = None) -> "DigitalProduct":
        if supplier is None:
            supplier = Supplier.from_dict(data.get("supplier", {}))
        return cls(
            prodID=data["prodID"],
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            download_size=data["download_size"],
            supplier=supplier,
        )

    def get_fulfilment_info(self) -> str:
        return "I am a product that must be downloaded"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["download_size"] = self.download_size
        return data


# ------------------------------------------------------------
# Aggregation: Inventory stores Product references.
# Removing a Product from Inventory does not destroy the Product.
# ------------------------------------------------------------

class Inventory:
    def __init__(self):
        self.products: list[Product] = []

    @property
    def items(self) -> list[Product]:
        """Compatibility alias for the original Lab 7 code."""
        return self.products

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def remove_product(self, product_id: str) -> Optional[Product]:
        product = self.find_product(product_id)
        if product is None:
            return None
        self.products.remove(product)
        return product

    def find_product(self, product_id: str) -> Optional[Product]:
        for product in self.products:
            if product_id.upper() == product.prodID.upper():
                return product
        return None

    # Retained as an alias so existing calls in the original program still work.
    def search_product(self, query: str) -> Optional[Product]:
        product = self.find_product(query)
        if product is None:
            print("Invalid Product ID")
        return product

    def display_all(self) -> None:
        if not self.products:
            print("There are no products in the inventory.")
            pause_program()
            return

        printHeader()
        for product in self.products:
            product.display_information()
            print(f"         Fulfilment: {product.get_fulfilment_info()}")
        pause_program()


# ------------------------------------------------------------
# Composition: Order creates and owns its OrderLine objects.
# Each OrderLine refers to a Product, but does not own it.
# ------------------------------------------------------------

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity


class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        # The Order creates the OrderLine, expressing composition.
        self.order_lines.append(OrderLine(product, quantity))

    def calculate_total(self) -> float:
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"\nOrder: {self.order_id}")
        if not self.order_lines:
            print("This order has no lines.")
        for line in self.order_lines:
            print(
                f"{line.product.name} x {line.quantity} "
                f"@ ${line.product.price:.2f} = ${line.calculate_subtotal():.2f}"
            )
        print(f"Order total: ${self.calculate_total():.2f}")


# ------------------------------------------------------------
# File handling
# ------------------------------------------------------------

class FileHandling:
    def __init__(self, path: str = "./inventory.json"):
        self.path: str = path

    def save_inventory(self, inventory: Inventory, deleted_ids: list[str]) -> None:
        package = {
            "inventory": [item.to_dict() for item in inventory.products],
            "deleted": deleted_ids,
        }
        try:
            with open(self.path, "w", encoding="utf-8") as file:
                json.dump(package, file, indent=4)
            print("Successfully saved to inventory.json")
        except (OSError, TypeError, ValueError) as error:
            print(f"Something went wrong\nError message: {error}")

    def load_inventory(self) -> tuple[Inventory, list[str]]:
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                package = json.load(file)
        except (ValueError, FileNotFoundError, OSError) as error:
            print(f"Could not load inventory: {error}. Starting empty.")
            package = {"inventory": [], "deleted": []}

        inventory = Inventory()
        for data in package.get("inventory", []):
            inventory.add_product(Product.from_dict(data))

        deleted_ids = package.get("deleted", [])
        return inventory, deleted_ids


# ------------------------------------------------------------
# Application setup and product creation
# ------------------------------------------------------------

storage = FileHandling()
inventory, deleted_ids = storage.load_inventory()


def generate_ID() -> str:
    if not inventory.products:
        current_id = 1
    else:
        current_id = max(
            int(product.prodID.removeprefix("P"))
            for product in inventory.products
        ) + 1

    new_id = f"P{current_id:04d}"
    while new_id in deleted_ids:
        current_id += 1
        new_id = f"P{current_id:04d}"
    return new_id


def generate_supplier_ID() -> str:
    supplier_numbers = [
        int(product.supplier.supplier_id.removeprefix("S"))
        for product in inventory.products
        if product.supplier.supplier_id.startswith("S")
        and product.supplier.supplier_id[1:].isdigit()
    ]
    return f"S{max(supplier_numbers, default=0) + 1:04d}"


def create_add_product(
    name: str, product_type: str, price: float, stock: int,
    size: float | int, supplier_name: str, supplier_email: str
) -> None:
    supplier = Supplier(generate_supplier_ID(), supplier_name, supplier_email)

    if product_type == "physical":
        new_product: Product = PhysicalProduct(
            generate_ID(), name, price, stock, float(size), supplier
        )
    else:
        new_product = DigitalProduct(
            generate_ID(), name, price, stock, int(size), supplier
        )

    inventory.add_product(new_product)
    print("Product has been added.")
    printHeader()
    new_product.display_information()
    pause_program()


def pid_lookup() -> Optional[Product]:
    query = input("Enter a valid Product ID: ").upper()
    result = inventory.find_product(query)
    if result is None:
        print("Invalid Product ID")
    return result


def update_product_stock() -> None:
    product = pid_lookup()
    if product is None:
        return
    product.update_stock(stockInput())
    pause_program()


def create_order() -> None:
    if not inventory.products:
        print("There are no products available to order.")
        pause_program()
        return

    order = Order(f"O{len(inventory.products) + 1:04d}")
    while True:
        product = pid_lookup()
        if product is None:
            break

        quantity = stockInput()
        if quantity == 0:
            print("Order quantity must be greater than zero.")
            continue

        order.add_order_line(product, quantity)
        if input("Add another item? [Y/N]: ").lower() != "y":
            break

    order.display_order()
    pause_program()


# ------------------------------------------------------------
# Main menu
# ------------------------------------------------------------

class MainMenu:
    def __init__(self):
        self.is_running: bool = True

    def display_menu(self) -> None:
        menu_options = """\
----- MENU -----
1. Display all products
2. Add new product
3. Update product stock
4. Product ID lookup
5. Save inventory
6. Create customer order
7. Exit program"""
        print(menu_options)

    def run(self) -> None:
        self.display_menu()
        while self.is_running:
            try:
                choice = int(input("\nSelect option: "))
            except ValueError:
                # INTENDED BEHAVIOUR: redisplay the menu after invalid input.
                self.display_menu()
                continue
            self.choice_handler(choice)

    def choice_handler(self, choice: int) -> None:
        match choice:
            case 1:
                inventory.display_all()
            case 2:
                create_add_product(*get_valid_input())
            case 3:
                update_product_stock()
            case 4:
                result = pid_lookup()
                if result is not None:
                    printHeader()
                    result.display_information()
                    print(result.supplier.display_information())
                    pause_program()
            case 5:
                storage.save_inventory(inventory, deleted_ids)
            case 6:
                create_order()
            case 7:
                self.is_running = False
            case _:
                # Keep the existing behaviour: invalid menu numbers redisplay it.
                self.display_menu()


if __name__ == "__main__":
    menu = MainMenu()
    menu.run()
