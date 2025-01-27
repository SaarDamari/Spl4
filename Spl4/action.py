from persistence import *
import sqlite3
import sys
from typing import List


def main(args: List[str]):
    print(sys.argv)
    inputfilename: str = args[1]
    
    # Open a single connection to the database
    conn = sqlite3.connect("bgumart.db")
    try:
        products = Dao(Product, conn)
        activities = Dao(Activitie, conn)
        
        with open(inputfilename) as inputfile:
            for line in inputfile:
                splittedline: List[str] = line.strip().split(", ")

                item_id = int(splittedline[0])  # Convert to int for SQL query
                quantity_item = int(splittedline[1])
                employee_id = int(splittedline[2])
                date = splittedline[3]

                try:
                    # Find the product by ID
                    result = products.find(id=item_id)
                    
                    if not result:  # If product does not exist
                        print(f"Error: Product with ID {item_id} does not exist.")
                        continue
                    for i in result:
                        print("result:", i)

                    current_quantity = result[0].quantity
                    print("current quan:", current_quantity)
                    print("item quan:", quantity_item)
                    # Check if the operation is valid
                    if current_quantity + quantity_item >= 0:
                        # Update product quantity
                        products.update(id=item_id, quantity=current_quantity + quantity_item)

                        # Insert into activities table
                        activity = Activitie(item_id, quantity_item, employee_id, date)
                        print(activity)
                        activities.insert(activity)
                        conn.commit()
                    else:
                        print(f"Error: Insufficient stock for product ID {item_id}.")
                
                except sqlite3.IntegrityError as e:
                    print(f"Error: Could not process activity. {e}")
        
    finally:
        cursor = conn.cursor()

        # Print Activities table
        print("Activities")
        cursor.execute('''
        SELECT *
        FROM activities
        ORDER BY "date"
        ''')
        for row in cursor.fetchall():
            print(row)
        print()
        # Ensure the connection is closed
        conn.close()


if __name__ == '__main__':
    main(sys.argv)
