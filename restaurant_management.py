import sqlite3

conn = sqlite3.connect('restaurant_database.db')

cursor = conn.cursor()

cursor.execute('''
  CREATE TABLE IF NOT EXISTS menu (
    id INT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    category VARCHAR(12) NOT NULL,
    price INT NOT NULL,
    status VARCHAR(13) NOT NULL
  )
''')

cursor.execute('''
  INSERT OR IGNORE INTO menu VALUES
  (1, "Shahi Paneer", "Veg", 650, "available"),
  (2, "Masala Dosa", "Veg", 600, "available"),
  (3, "Chicken Biryani", "Non-Veg", 850, "available"),
  (4, "Butter Chicken", "Non-Veg", 750, "not available"),
  (5, "Veg Biryani", "Veg", 550, "available"),
  (6, "Paneer Tikka", "Starter", 400, "available"),
  (7, "Chicken Tikka", "Starter", 500, "not available"),
  (8, "French Fries", "Fast Food", 200, "available"),
  (9, "Veg Burger", "Fast Food", 250, "available"),
  (10, "Chicken Burger", "Fast Food", 350, "not available"),
  (11, "Margherita Pizza", "Pizza", 450, "available"),
  (12, "Farmhouse Pizza", "Pizza", 600, "available"),
  (13, "White Sauce Pasta", "Pasta", 400, "not available"),
  (14, "Red Sauce Pasta", "Pasta", 380, "available"),
  (15, "Masala Chai", "Beverage", 50, "available"),
  (16, "Cold Coffee", "Beverage", 150, "not available"),
  (17, "Fresh Lime Soda", "Beverage", 100, "available"),
  (18, "Chocolate Milkshake", "Beverage", 180, "available"),
  (19, "Gulab Jamun", "Dessert", 120, "available"),
  (20, "Chocolate Brownie", "Dessert", 200, "not available"),
  (21, "Vanilla Ice Cream", "Dessert", 100, "available"),
  (22, "Rasgulla", "Dessert", 100, "available"),
  (23, "Idli Sambar", "South Indian", 180, "available"),
  (24, "Medu Vada", "South Indian", 150, "not available"),
  (25, "Chole Bhature", "North Indian", 250, "available"),
  (26, "Dal Makhani", "North Indian", 350, "available"),
  (27, "Hakka Noodles", "Chinese", 300, "not available"),
  (28, "Veg Manchurian", "Chinese", 320, "available"),
  (29, "Fish Curry", "Seafood", 700, "not available"),
  (30, "Prawn Masala", "Seafood", 900, "available")
''')

conn.commit()

cursor.execute('''
  CREATE TABLE IF NOT EXISTS restaurant_tables (
    table_id CHAR(3) PRIMARY KEY,
    seats INT NOT NULL,
    state VARCHAR(9) NOT NULL,
    order_id VARCHAR(5),
    since TIME
  )
''')

cursor.execute('''
  INSERT OR IGNORE INTO restaurant_tables VALUES
  ("T01", 2, "Available", NULL, NULL),
  ("T02", 2, "Available", NULL, NULL),
  ("T03", 4, "Available", NULL, NULL),
  ("T04", 4, "Available", NULL, NULL),
  ("T05", 4, "Available", NULL, NULL),
  ("T06", 4, "Available", NULL, NULL),
  ("T07", 6, "Available", NULL, NULL),
  ("T08", 6, "Available", NULL, NULL),
  ("T09", 8, "Available", NULL, NULL),
  ("T10", 8, "Available", NULL, NULL)
''')

conn.commit()

def view_table_status():
  print(f"\n{'TABLE STATUS'.center(46)}")
  print("-"*46)
  print(f"{'TABLE_ID':<9} {'SEATS':<6} {'STATE':<10} {'ORDER_ID':<9} SINCE")
  print("-"*46)
  
  available_count = 0
  occupied_count = 0
  
  cursor.execute("SELECT * FROM restaurant_tables")
  for row in cursor.fetchall():
    if row[2] == "Occupied":
      state = f"\x1b[31m{row[2]}\x1b[0m  "
      occupied_count += 1
    else:
      state = row[2]
      available_count += 1
      
    if row[3] is not None:
      order_id = row[3].center(8)
    else:
      order_id = "--".center(8)
      
    if row[4] is not None:
      since = row[4]
    else:
      since = "--".center(8)
      
    print(f"{row[0]:<9} {row[1]:<6} {state:<10} {order_id:<9} {since}")
    
  print("-"*46)
  print("\x1b[1;36m" + f"Available: {available_count}  •  Occupied: {occupied_count}".center(46) + "\x1b[0m")
  print("-"*46)

def view_all_items():
  print(f"\n{'RESTAURANT MENU'.center(61)}")
  print("-"*61)
  print(f"{'ID':<3} {'ITEM NAME':<22} {'CATEGORY':<13} {'PRICE':<6} {'STATUS':<14}")
  print("-"*61)

  item_count = 0
  available_count = 0
  not_available_count = 0
  
  cursor.execute("SELECT * FROM menu")
  for row in cursor.fetchall():
    if row[4] == "not available":
      status = f"\x1b[31m{row[4]}\x1b[0m"
      not_available_count += 1
    else:
      status = row[4]
      available_count += 1

    print(f"{row[0]:<3} {row[1]:<22} {row[2]:<13} ₹{row[3]:<5} {status}")
    item_count += 1
    
  if item_count == 0:
    print(f"\n\x1b[1;31m{'Menu is currently empty!'.center(61)}\x1b[0m\n")
  
  print("-"*61)
  print("\x1b[1;36m" + f"Items: {item_count}  •  Available: {available_count}  •  Not Available: {not_available_count}".center(61) + "\x1b[0m")
  print("-"*61)

def view_items_by_category(category):
  print(f"\n{('Category: ' + category).center(61)}")
  print("-"*61)
  print(f"{'ID':<3} {'ITEM NAME':<22} {'CATEGORY':<13} {'PRICE':<6} {'STATUS':<14}")
  print("-"*61)

  item_count = 0
  available_count = 0
  not_available_count = 0
  
  cursor.execute("SELECT * FROM menu WHERE category = ?", (category,))
  for row in cursor.fetchall():
    if row[4] == "not available":
      status = f"\x1b[31m{row[4]}\x1b[0m"
      not_available_count += 1
    else:
      status = row[4]
      available_count += 1

    print(f"{row[0]:<3} {row[1]:<22} {row[2]:<13} ₹{row[3]:<5} {status}")
    item_count += 1

  print("-"*61)
  print("\x1b[1;36m" + f"Items: {item_count}  •  Available: {available_count}  •  Not Available: {not_available_count}".center(61) + "\x1b[0m")
  print("-"*61)

def add_new_item(id, name, category, price, status):
  cursor.execute("INSERT INTO menu VALUES (?, ?, ?, ?, ?)", (id, name, category, price, status))
  conn.commit()
  print("\n\x1b[1;32mThe item has been successfully added.\x1b[0m")

def edit_menu_item(new_id, new_name, new_category, new_price, id):
  cursor.execute("UPDATE menu SET id = ?, name = ?, category = ?, price = ? WHERE id = ?", (new_id, new_name, new_category, new_price, id))
  conn.commit()
  print(f"\n\x1b[1;32mThe item has been successfully edited.\x1b[0m")

def get_item_details(id):
  cursor.execute("SELECT * FROM menu WHERE id = ?", (id,))
  item = cursor.fetchall()

  print(f"\n\x1b[36m{'ITEM SUMMARY'.center(15)}")
  print(f"ID       : {item[0][0]}")
  print(f"Name     : {item[0][1]}")
  print(f"Category : {item[0][2]}")
  print(f"Price    : ₹{item[0][3]}")
  print(f"Status   : {item[0][4]}\x1b[0m\n")

def change_item_status(id, status):
  cursor.execute("UPDATE menu SET status = ? WHERE id = ?", (status, id))
  conn.commit()
  print(f"\n\x1b[1;32mThe item status has been successfully updated.\x1b[0m")

def delete_menu_item(id):
  cursor.execute("DELETE FROM menu WHERE id = ?", (id,))
  conn.commit()
  print("\n\x1b[1;32mThe item has been successfully deleted.\x1b[0m")

def menu_management():
  while True:
    heading = "\x1b[4mMENU MANAGEMENT\x1b[0m"
    print(f"\n{heading.center(44)}\n")
    print("1. View All Items")
    print("2. View Items by Category")
    print("3. Add New Item")
    print("4. Edit Menu Item")
    print("5. Manage Item Availability")
    print("6. Delete Menu Item")
    print("7. Back to Main Menu\n")

    choice = input("Enter your choice [1-7]: ")

    if choice == '1':
      view_all_items()
    elif choice == '2':
      print("\nSelect a category from the options below:")
      cursor.execute("SELECT DISTINCT category FROM menu")
      categories = cursor.fetchall()
      
      for n, category in enumerate(categories):
        print(f"{n+1}. {category[0]}")

      running = True
      while running:
        category = input("\nEnter your category name [e.g: Dessert]: ").title()
        for tuple in categories:
          if category in tuple:
            view_items_by_category(category)
            running = False
            break
        else:
          print("\n\x1b[1;31mCategory Not Found!\x1b[0m")
    elif choice == '3':
      id = int(input("\nAllocate a unique ID to your item: "))
      name = input("\nEnter the item name: ").title()
      
      print("\nSelect one category from the existing options or create a new one:")
      cursor.execute("SELECT DISTINCT category FROM menu")
      categories = cursor.fetchall()
      for n, category in enumerate(categories):
        print(f"{n+1}. {category[0]}")

      category = input("\nEnter your category name [e.g: Dessert]: ").title()
      for tuple in categories:
        if category in tuple:
          break
      else:
        print("\n\x1b[1;32mThe new category has been created and selected for your item.\x1b[0m")

      price = int(input("\nEnter the price of your item: ₹"))

      while True:
        status = str(input("\nIs the item currently available [yes/no]: ")).lower()
        if status == "yes":
          status = "available"
          break
        elif status == "no":
          status = "not available"
          break
        else:
          print("\n\x1b[1;31mInvalid Choice! Enter 'yes' if available, or 'no' if not.\x1b[0m")

      print(f"\n\x1b[36m{'ITEM SUMMARY'.center(15)}")
      print(f"ID       : {id}")
      print(f"Name     : {name}")
      print(f"Category : {category}")
      print(f"Price    : ₹{price}")
      print(f"Status   : {status}\x1b[0m\n")

      print("Add this item?")
      print("1. Confirm")
      print("2. Cancel")

      while True:
        choice = input("\nEnter your choice [1-2]: ")

        if choice == '1':
          add_new_item(id, name, category, price, status)
          break
        elif choice == '2':
          break
        else:
          print("\x1b[1;31m\nInvalid Choice!\x1b[0m")
    elif choice == '4':
      id = int(input("\nEnter the item ID: "))
      cursor.execute("SELECT * FROM menu WHERE id = ?", (id,))
      item = cursor.fetchall()

      print("\n\x1b[1;36mCurrent values are in brackets. Press ENTER to keep them.\x1b[0m")
      new_id = input(f"Allocate a new unique ID to your item \x1b[1;36m[{id}]\x1b[0m: ")
      if not new_id:
        new_id = id

      new_name = input(f"\nEnter the item new name \x1b[1;36m[{item[0][1]}]\x1b[0m: ").title()
      if not new_name:
        new_name = item[0][1]

      print("\nSelect one category from the existing options or create a new one:")
      cursor.execute("SELECT DISTINCT category FROM menu")
      categories = cursor.fetchall()
      for n, category in enumerate(categories):
        print(f"{n+1}. {category[0]}")
        
      new_category = input(f"\nEnter your new category name \x1b[1;36m[{item[0][2]}]\x1b[0m: ").title()
      if not new_category:
        new_category = item[0][2]
      else:
        for tuple in categories:
          if new_category in tuple:
            break
        else:
          print("\n\x1b[1;32mThe new category has been created and selected for your item.\x1b[0m")

      new_price = input(f"\nEnter the new price of your item \x1b[1;36m[₹{item[0][3]}]\x1b[0m: ₹")
      if not new_price:
        new_price = item[0][3]

      print(f"\n\x1b[36m{'ITEM SUMMARY'.center(15)}")
      print(f"ID       : {new_id}")
      print(f"Name     : {new_name}")
      print(f"Category : {new_category}")
      print(f"Price    : ₹{new_price}")
      print(f"Status   : {item[0][4]}\x1b[0m\n")

      print("Edit this item?")
      print("1. Confirm")
      print("2. Cancel")

      while True:
        choice = input("\nEnter your choice [1-2]: ")

        if choice == '1':
          edit_menu_item(int(new_id), new_name, new_category, int(new_price), id)
          break
        elif choice == '2':
          break
        else:
          print("\x1b[1;31m\nInvalid Choice!\x1b[0m")
    elif choice == '5':
      id = int(input("\nEnter the item ID: "))
      get_item_details(id)
      print("Select the item status:")
      print("1. available")
      print("2. not available")

      while True:
        choice = input("\nEnter your choice [1-2]: ")
        if choice == '1':
          change_item_status(id, status="available")
          break
        elif choice == '2':
          change_item_status(id, status="not available")
          break
        else:
          print("\x1b[1;31m\nInvalid Choice!\x1b[0m")
    elif choice == '6':
      id = int(input("\nEnter the item ID: "))
      get_item_details(id)
      print("Are you sure you want to delete?")
      print("1. Confirm")
      print("2. Cancel")

      while True:
        choice = input("\nEnter your choice [1-2]: ")
        if choice == '1':
          delete_menu_item(id)
          break
        elif choice == '2':
          break
        else:
          print("\x1b[1;31m\nInvalid Choice!\x1b[0m")
    elif choice == '7':
      break
    else:
      print("\x1b[1;31m\nInvalid Choice!\x1b[0m")

def main():
  while True:
    print(f"\n{'WELCOME TO'.center(44)}")
    print("RESTAURANT MANAGEMENT SYSTEM".center(44))
    print("\n1. New Order")
    print("2. View & Edit Orders")
    print("3. Billing & Payment")
    print("4. View Table Status")
    print("5. Menu Management")
    print("6. Feedback")
    print("7. Exit\n")

    choice = input("Enter your choice [1-7]: ")

    if choice == '1':
      pass
    elif choice == '2':
      pass
    elif choice == '3':
      pass
    elif choice == '4':
      view_table_status()
    elif choice == '5':
      menu_management()
    elif choice == '6':
      pass
    elif choice == '7':
      break
    else:
      print("\x1b[1;31m\nInvalid Choice!\x1b[0m")

if __name__ == "__main__":
  main()
