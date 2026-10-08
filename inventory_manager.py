import json

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
    new_product =  {
        "prodID": generate_ID(),
        "name": name,
        "price": price,
        "stock": stock
    }
    inventory.append(new_product)
    return
    # return # return new item (dict) OR automatically append to list, return none

def update_stock(): # takes PID
    product = pid_lookup()
    if product == False:
        return
    # if this point is reached, product is valid
    print(f"Updating quantity of {product["name"]}")
    new = stockInput()
    product["stock"] = new

    ### TODO: PLACEHOLDER FOR DISPLAY FUNCTION
    print("Product updated")
    return

def pid_lookup():
    query = input("Enter a valid Product ID: ").upper()
    for item in inventory:
        if query == item["prodID"]:
            return item # returns product dictionary
    print("Invalid Product ID.")
    return False

def search_product(): # takes PID
    product = pid_lookup()
    print(f"ID\tName\t\tPrice\tQuantity")
    for i in product: print(product[i], end="\t")
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
                display_product("all")
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

def priceInput():
    while True:
        try: 
            price = float(input("Enter product price: "))
            break
        except ValueError: 
            print("Your price must be a valid number!")
    return price

def stockInput():
    while True:
        try: 
            stock = int(input("Enter stock quanity: "))
            break
        except ValueError: 
            print("Stock must be a valid integer!")
    return stock

def get_valid_input():
    name = input("Enter product name: ")
    price = priceInput()
    stock = stockInput()
    return name, price, stock 



savefile = load_inventory()
inventory = savefile["inventory"]
deleted_ids = savefile["deleted"]

def generate_ID(deleted=deleted_ids, inventory=inventory): # returns a new unique ID
    
    #gets current id index
    
    if(len(inventory)) == 0:
        currentID = 1
    else:
        currentID = int(inventory[len(inventory)-1]["prodID"].strip('P'))
        #icr by 1
        currentID += 1
    
    #format as ID
    newID = "P" + f"{currentID:04d}"
    while newID in deleted:
        currentID +=1 
        newID = "P" + f"{currentID:04d}"
    return newID


program_menu()