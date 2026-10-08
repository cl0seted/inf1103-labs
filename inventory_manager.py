deleted_ids = ["P0004"]
products = [
    {"prodID":"P0001", "name":"Digital Piano","price":300,"stock":20},
    {"prodID":"P0002", "name":"Electric Guitar","price":150,"stock":10},
    {"prodID":"P0003", "name":"Kalimba","price":25,"stock":7},
]

def create_add_product(name, price, stock): # takes user input, creates dict for new item
    return {
        "prodID": "????", # TODO: how should we generate product ID? Align with list? What if delete?
        "name": name,
        "price": price,
        "stock": stock
    }
    # return # return new item (dict) OR automatically append to list, return none

def update_stock(): # takes PID
    # index the array for matching PID
    return

def search_product(): # takes PID
    return

def display_all():
    # print all items in array; formatted
    return

def save_inventory(): # takes the array with products
    return

def load_inventory(): # loads products from .json file
    return

def program_menu(): # Function that handles program options
    return

# new_product = {
#     "prodID": "P0001", # product ID
#     "name": "Potato", # Product name 
#     "price": 500.00, # Price in 2dp
#     "stock": 10 # Product quantity
# }

name = "Laptop"
price = 500
stock = 20

print(products)

dummy = create_add_product(name, price, stock) # returns dict item
print(dummy)

