deleted_ids = ["P0004","P0005","P0006"]
products = [
    {"prodID":"P0001", "name":"Digital Piano","price":300,"stock":20},
    {"prodID":"P0002", "name":"Electric Guitar","price":150,"stock":10},
    {"prodID":"P0003", "name":"Kalimba","price":25,"stock":7},
]

def generate_ID(deleted=deleted_ids, inventory=products): # returns a new unique ID
    #gets current id index
    currentID = int(products[len(products)-1]["prodID"].strip('P'))
    
    #icr by 1
    currentID += 1
    
    #format as ID
    newID = "P" + f"{currentID:04d}"
    while newID in deleted:
        currentID +=1 
        newID = "P" + f"{currentID:04d}"
    return newID

def create_add_product(name, price, stock): # takes user input, creates dict for new item
    new_product =  {
        "prodID": generate_ID(),
        "name": name,
        "price": price,
        "stock": stock
    }
    products.append(new_product)
    return
    # return # return new item (dict) OR automatically append to list, return none

def update_stock(): # takes PID
    # index the array for matching PID
    return

def search_product(): # takes PID
    query = input("Enter a valid Product ID: ").upper()
    # if query.upper() not in inventory
    for item in products:
        if query == item["prodID"]:
            print(f"ID\tName\t\tPrice\tQuantity")
            for i in item: print(item[i], end="\t")
            return
    print("Invalid Product ID.")
    return 

def display_all():
    # print all items in array; formatted
    return

def save_inventory(): # takes the array with products
    return

def load_inventory(): # loads products from .json file
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
                print(products) # to be fleshed out
            case 2:
                create_add_product(*get_valid_input())
            case 4:
                search_product()
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

# new_product = {
#     "prodID": "P0001", # product ID
#     "name": "Potato", # Product name 
#     "price": 500.00, # Price in 2dp
#     "stock": 10 # Product quantity
# }


program_menu()
# search_product()