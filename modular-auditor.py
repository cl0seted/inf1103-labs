########################
### ASSUMPTIONS MADE ###
########################
# Due to ambiguous or unspecified requirements in the labsheet,
# this code makes the following assumptions:
# 1) "One delivery" contains only one stock unit
# 2) One stock unit costs $250, and tax does not include any other fees

inventory = 0
failed_inputs = 0
new_processed = 0

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

while True:
    prompt = get_valid_input()
    match prompt:
        case False:
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
                new_processed += prompt
                print(f'Added {prompt} into the inventory.\nNew inventory count: {inventory}\n')
                print(f'Newly added stocks cost ${taxes:.2f} in taxes.\n')
    
    if inventory > 500:
        print("---ALERT!!!---\nYou have exceeded the maximum limit for this stock. The program will now exit.")
        break

report = generate_report(inventory, failed_inputs)
print(report)