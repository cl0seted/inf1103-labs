import json

def printHeader():
    print(f"{'ID':<5} | {'Name':<15} | {'Price':<8} | {'Quantity':<4}")

def stockInput():
    while True:
        try: 
            stock = int(input("Enter stock quanity: "))
            break
        except ValueError: 
            print("Stock must be a valid integer!")
    return stock

# create a class for products
class Product:
    def __init__(self, prodID:str, name:str, price:float, stock:int):
        self.prodID = prodID
        self.name = name
        self.price = price
        self.stock = stock

    def update_stock(self, quanity:int) -> None:
        print(f"Updating quantity of {self.name}")
        new = stockInput()
        self.stock = new

        ### TODO: PLACEHOLDER FOR DISPLAY FUNCTION
        print("Product updated")

    def display_information(self) -> None:
        print(f"{self.prodID:<5} | {self.name:<15} | ${self.price:<8.2f}| {self.stock:<4}")


class Inventory:
    def __init__(self):
        self.items = [] # array to keep all child classes

    def add_product(self, product: Product) -> None:
        self.items.append(product) 

    def search_product(self, query:str) -> None:
        for i in self.items:
            if query.upper() == i.prodID:
                printHeader()
                i.display_information()
                return
        print("Invalid Product ID.")
            
    
    def display_all(self) -> None:
        printHeader()
        for i in self.items:
            i.display_information()


deleted_ids = []

# --- TEMP PLACEHOLDER FOR REFERENCE ---
inventory = Inventory()
product1 = Product("P0001", "Laptop", 1200.00, 15) # creating product from Product class, via init
product2 = Product("P0002", "Mouse", 25.50, 40)
inventory.add_product(product1) # pass the product to inventory class to store in a list
inventory.add_product(product2)

# inventory.search_product("p0003")
# inventory.display_all()


# for i in inventory.items:
#     print(i.name)

def save_inventory(inventory,deleted_ids):
    package = {
        "inventory":inventory,
        "deleted":deleted_ids 
    }
    try:
        # open/create inv file. Overwrite with new data
        with open("./inventory.json","w") as file:
            json.dump(package, file, indent=4)
            print("Succesfully saved to inventory.json")
    except Exception as error_code:
        fail = f"Something went wrong\nError message: {error_code}"
        print(fail)
    return

def load_inventory():
    try:
        with open("inventory.json","r") as file:
            try:
                my_dict = json.load(file)
                return my_dict
            except ValueError as error_code: # Error reading inventory file (either corrupted or empty)
                fail = f"Something went wrong - 1\nError message: {error_code}"
                print(f"{fail}\n Initializing empty inventory")
                return {"inventory": [], "deleted": []}
    except FileNotFoundError as error_code: # Inventory file not exists
        fail = f"Something went wrong - 2\nError message: {error_code}"
        print(f"{fail}\n Initializing empty inventory")
        return {"inventory": [], "deleted": []}
        

def create_add_product(name, price, stock): # takes user input, creates dict for new item
    new_product = Product(generate_ID(), name, price, stock)
    inventory.add_product(new_product)
    return


def display_product(product=""):
    # print("-" * 20)
    if product == "all":
        print(f"{'ID':<5} | {'Name':<15} | {'Price':<8} | {'Quantity':<4}")
        for product in inventory:
            print(f"{product["prodID"]:<5} | {product["name"]:<15} | ${product["price"]:<8.2f}| {product["stock"]:<4}")
    else:
        product = pid_lookup() # returns a dictionary product
        if product == False:
            return
        print(f"{'ID':<5} | {'Name':<15} | {'Price':<8} | {'Quantity':<4}")
        print(f"{product["prodID"]:<5} | {product["name"]:<15} | ${product["price"]:<8.2f}| {product["stock"]:<4}")
    return


def priceInput():
    while True:
        try: 
            price = float(input("Enter product price: "))
            break
        except ValueError: 
            print("Your price must be a valid number!")
    return price


def get_valid_input():
    name = input("Enter product name: ")
    price = priceInput()
    stock = stockInput()
    return name, price, stock 

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

# savefile = load_inventory()
# inventory = savefile["inventory"]
# deleted_ids = savefile["deleted"]


def program_menu(): # Function that handles program options
    menu_options = """\n----- MENU -----\n1. Display all products\n2. Add new product\n3. Update product stock\n4. Product ID lookup\n5. Save inventory\n6. Exit program"""
    print(menu_options)
    while True:
        try: choice = int(input("\nSelect option: "))
        except ValueError:
            print(menu_options)
            continue

        match choice:
            case 1:
                # display_product("all")
                inventory.display_all()
            case 2:
                create_add_product(*get_valid_input())
            case 3:
                update_stock()
            case 4:
                display_product()
            case 5:
                save_inventory(inventory,deleted_ids)
            case 6:
                break
            case _: # default case
                print(menu_options)
    return


program_menu()

# print(generate_ID())


# def update_stock(): # takes PID
#     product = pid_lookup()
#     if product == False:
#         return
#     # if this point is reached, product is valid
#     print(f"Updating quantity of {product["name"]}")
#     new = stockInput()
#     product["stock"] = new

#     ### TODO: PLACEHOLDER FOR DISPLAY FUNCTION
#     print("Product updated")
#     return


# def pid_lookup():
#     query = input("Enter a valid Product ID: ").upper()
#     for item in inventory:
#         if query == item["prodID"]:
#             return item # returns product dictionary
#     print("Invalid Product ID.")
#     return False

# def search_product(): # takes PID
#     product = pid_lookup()
#     print(f"ID\tName\t\tPrice\tQuantity")
#     for i in product: print(product[i], end="\t")
#     return 