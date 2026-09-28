########################
### ASSUMPTIONS MADE ###
########################
# Due to ambiguous or unspecified requirements in the labsheet,
# this code makes the following assumptions:
# 1) This script will deviate from the sample output provided in Week 4 Labsheet
# 2) Instead of tracking products and its quantity, this script will only track new stock quantities

failed_inputs = 0

def load_inventory():
    try:
        with open("inventory.txt","r") as file:
            try:
                content = file.read().split("\n")
                # content[0] is inventory value
                # content[1] is history array
                hist = content[1].strip("[]").split(",")
                cleaned_hist = [int(item) for item in hist]
                return int(content[0]), cleaned_hist # return the inventory value and history
            except ValueError: # Error reading inventory file (either corrupted or empty)
                return 0, []
    except FileNotFoundError: # Inventory file not exists
        return 0, []
    

def save_inventory(total_stocks, new_intake):
    try:
        # open/create inv file. Overwrite with new data
        with open("inventory.txt","w") as file:
            file.write(f"{total_stocks}\n{new_intake}")
    except Exception as error_code:
        fail = f"Something went wrong\nError message: {error_code}"
        print(fail)
    return

def get_valid_input():
    new = input(f"Current inventory count: {inventory}\nPlease input how many stocks we received today: ")
    if new.lower() == "quit": 
        return False # quit signal
    
    try:
        new = int(new) 
    except ValueError:
        print("Please input an integer, or type 'quit' to quit") 
        return None # send a fail signal
    
    match new:
        case val if val < 0:
            print("Negative values are not allowed!")
            return None # send a fail signal
        case _:
            return new

def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total

def calculate_tax(amount):
    stock_price = 250 # Assume each stock is 250 dollars
    tax = round(stock_price * amount * 0.1, 2) # calculate tax, round to 2dp
    return tax

def generate_report(total_units, failed_attempts):
    final_report = f'Total units processed: {total_units}\nNumber of failed inputs this session: {failed_attempts}\n\nQuitting program...'
    return final_report

# Initialize inventory var and history list; get value from txt
inventory, history = load_inventory()

while True:
    prompt = get_valid_input()
    match prompt:
        case False: # Quit signal received
            break
        case None:
            failed_inputs += 1
        case _:
            # if code reaches here, is a valid numerical stock input
            total = process_delivery(inventory, prompt) # parse old inv and new stock into func
            if total == inventory:
                continue # ignore further processing if no new stocks (User inputs 0)
            else:
                inventory = total
                taxes = calculate_tax(prompt)
                history.append(prompt) # Add new stock into history
                print(f'Added {prompt} into the inventory.\nNew inventory count: {inventory}\n')
                print(f'Newly added stocks cost ${taxes:.2f} in taxes.\n')
    
    if inventory > 500:
        print("---ALERT!!!---\nYou have exceeded the maximum limit for this stock. The program will now exit.")
        break
save_inventory(inventory,history)


report = generate_report(inventory, failed_inputs)
print(report)