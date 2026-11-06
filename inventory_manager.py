from abc import ABC, abstractmethod
import json

def printHeader():
    print(f"{'ID':<5} | {'Name':<15} | {'Price':<8} | {'Quantity':<4}")

def stockInput():
    while True:
        try: 
            stock = int(input("Enter stock quantity: "))
            break
        except ValueError: 
            print("Stock must be a valid integer!")
    return stock

def pause_program():
    input("Press enter to continue:")

# create a class for products
class Product(ABC):
    def __init__(self, prodID:str, name:str, price:float, stock:int):
        self.prodID = prodID
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quantity:int) -> None:
        print(f"Updating quantity of {self.name}")
        # new = stockInput()
        self.stock = quantity
        print("Product updated")

    def to_dict(self) -> dict:
        return {
            "prodID": self.prodID,
            "type": appendType(self),
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }

    @classmethod
    def from_dict(cls, data:dict):

        product_type = data["type"]

        if product_type == "physical":
            return PhysicalProduct.from_dict(data)

        if product_type == "digital":
            return DigitalProduct.from_dict(data)

        else:
            raise ValueError(f"Unknown product type: {product_type}")

    @abstractmethod
    def display_information(self) -> None:
        productinfo = f"{self.prodID:<5} | {self.name:<15} | ${self.price:<8.2f}| {self.stock:<8}"
        # print(productinfo)
        return productinfo

    @abstractmethod
    def get_fulfilment_info(self):
        pass

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, prodID:str, name:str, price:float, stock:int, weight:float):
        super().__init__(prodID, name, price, stock) # steals details from parent class
        self.weight = weight

    def display_information(self) -> None:
        productinfo = super().display_information()
        extrainfo = f" | --- Product weight  : {self.weight}kg / unit"
        productinfo += extrainfo
        print(f"{productinfo}")
    
    @classmethod
    def from_dict(cls, data:dict) -> PhysicalProduct:
        return cls(
            prodID = data["prodID"],
            name = data["name"],
            price = data["price"],
            stock = data["stock"],
            weight = data["weight"]
        )

    def get_fulfilment_info(self):
        return "I am a product that must be shipped"

    def calculate_shipping_cost(self):
        cost = round(self.weight * 0.7,2) # shipping cost is 10%, tax is 7%
        return cost
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data["weight"] = self.weight
        return data



class DigitalProduct(Product):
    def __init__(self, prodID:str, name:str, price:float, stock:int, download_size:int):
        super().__init__(prodID, name, price, stock) # steals details from parent class
        self.download_size = download_size

    def display_information(self) -> None:
        productinfo = super().display_information()
        extrainfo = f" | --- Product filesize: {self.download_size} Mb"
        productinfo += extrainfo
        print(f"{productinfo}")
        return

    @classmethod
    def from_dict(cls, data:dict) -> DigitalProduct:
        return cls(
            prodID = data["prodID"],
            name = data["name"],
            price = data["price"],
            stock = data["stock"],
            download_size = data["download_size"]
        )

    def get_fulfilment_info(self):
        return "I am a product that must be downloaded"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["download_size"] = self.download_size
        return data

class Inventory:
    def __init__(self):
        self.items = [] # array to keep all child classes

    def add_product(self, product: Product) -> None:
        self.items.append(product) 

    def search_product(self, query:str) -> Product | None:
        for i in self.items:
            if query.upper() == i.prodID:
                return i
        print("Invalid Product ID")
        return None
            
    def display_all(self) -> None:
        printHeader()
        for i in self.items:
            i.display_information()
        pause_program()

def appendType(item):
    return item.__class__.__name__.lower().replace("product","")


class FileHandling:
    def __init__(self):
        self.path = "./inventory.json"

    def save_inventory(self, inventory, deleted_ids:list):
        package = {
            "inventory": [
            item.to_dict() for item in inventory.items
            ],
            "deleted": deleted_ids
        }
        try:
            with open(self.path, "w") as file:
                json.dump(package, file, indent=4)
                print("Successfully saved to inventory.json")
        except Exception as error_code:
            fail = f"Something went wrong\nError message: {error_code}"
            print(fail)

    def load_inventory(self):
        try:
            with open(self.path, "r") as file:
                package = json.load(file)
        except ValueError as error: # Error reading inventory (corrupted or empty)
            print(f"Could not load inventory: {error}\n. Starting empty")
            package = {"inventory": [], "deleted": []}
        
        except FileNotFoundError:
            print(f"Inventory file not found. Starting empty")
            package = {"inventory": [], "deleted": []}
        
        inventory = Inventory()

        for data in package["inventory"]:
            inventory.add_product(Product.from_dict(data))

        deleted_ids = package["deleted"]
        
        return inventory, deleted_ids

storage = FileHandling()
inventory, deleted_ids = storage.load_inventory()

def create_add_product(name, product_type, price, stock, size): # takes user input, creates dict for new item
    
    if product_type == "physical":
        new_product = PhysicalProduct(generate_ID(), name, price, stock, size) #MISSING WEIGHT
    if product_type == "digital":
        new_product = DigitalProduct(generate_ID(), name, price, stock, size) #MISSING FILESIZE
    
    inventory.add_product(new_product)
    print("Product has been added.")
    
    printHeader()
    new_product.display_information()
    pause_program()
    return


def priceInput():
    while True:
        try: 
            price = float(input("Enter product price: "))
            break
        except ValueError: 
            print("Your price must be a valid number!")
    return price

def sizeInput(product_type):
    while True:
        if product_type == "physical":
            prompt = "Enter product weight in kilograms: "
            try: 
                size = float(input(prompt))
                break
            except ValueError: 
                print("Please input a value up to two decimal places.")

        if product_type == "digital":
            prompt = "Enter product filesize in megabytes: "
            try: 
                size = int(input(prompt))
                break
            except ValueError: 
                print("Please input a valid integer.")
    return size


def get_valid_input():
    match input("Enter product type: [P]hysical [D]igital\nChoice: ").lower():
        case "p":
            product_type = "physical"
        case "d":
            product_type = "digital"
        case _:
            print("Defaulting to product type: Physical")
            product_type = "physical"
    name = input("Enter product name: ")
    size = sizeInput(product_type)
    price = priceInput()
    stock = stockInput()
    return name, product_type, price, stock, size

def generate_ID(deleted=deleted_ids, inventory=inventory.items): # returns a new unique ID
    #gets current id index
    if(len(inventory)) == 0:
        currentID = 1
    else:
        currentID = int(inventory[len(inventory)-1].prodID.strip('P'))
        #icr by 1
        currentID += 1

    #format as ID
    newID = "P" + f"{currentID:04d}"
    while newID in deleted:
        currentID +=1 
        newID = "P" + f"{currentID:04d}"
    return newID

def pid_lookup():
    query = input("Enter a valid Product ID: ").upper()
    search_result = inventory.search_product(query)
    return search_result


class MainMenu:
    def __init__ (self):
        self.is_running = True

    def display_menu(self):
        menu_options = """\n----- MENU -----\n1. Display all products\n2. Add new product\n3. Update product stock\n4. Product ID lookup\n5. Save inventory\n6. Exit program"""    
        print(menu_options)

    def run(self):
        self.display_menu()
        while self.is_running:
            try: choice = int(input("\nSelect option: "))
            except ValueError:
                self.display_menu()
                continue
            self.choice_handler(choice)
    
    def choice_handler(self, choice):
        match choice:
            case 1:
                inventory.display_all()
            case 2:
                create_add_product(*get_valid_input())
            case 3:
                query = pid_lookup()
                query.update_stock(stockInput())
            case 4:
                if (result := pid_lookup()) is not None:
                    printHeader()
                    result.display_information()
                    pause_program()
            case 5:
                storage.save_inventory(inventory, deleted_ids)
            case 6:
                self.is_running = False
            case _: # default case
                self.display_menu()


menu = MainMenu()
menu.run()