
# Task 1: initialize inventory to 0
inventory = 0
failed_inputs = 0
new_processed = 0

# Task 2: Initiate an infinite loop
while True:
    new = input(f"Current inventory count: {inventory}\nPlease input how many stocks we received today: ")
    if new.lower() == "quit": 
        break
    
    # If this point is reached, new is not a quit event

    try:
        new = int(new) # Task 3: Accept stock values as integers
    except ValueError:
        # Task 4: Handle invalid input
        print("Please input an integer, or type 'quit' to quit")
        failed_inputs += 1 # Task 8: Report failed entries
        continue # skip everything and return to the start of the loop

    # Task 5: Reject negative numbers
    if new < 0:
        print("Negative values are not allowed!")
        failed_inputs += 1 # Task 8: Report failed entries
        continue 

    new_processed += new # Task 9: Report the total units processed
    inventory += new # Task 6: Keep a running total of inventory

    print(f'Added {new} into the inventory.\n\nNew inventory count: {inventory}\n')
    
    # Task 7: Trigger an overstock alert
    if inventory > 500:
        print("---ALERT!!!---\nYou have exceeded the maximum limit for this stock. The program will now exit.")
        break
    
print(f'Total units processed: {new_processed}\nFinal inventory count: {inventory}\nNumber of failed inputs this session: {failed_inputs}\n\nQuitting program...')