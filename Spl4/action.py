from persistence import *
import sqlite3
import sys
from typing import List

def main(args: List[str]):
    print(sys.argv)
    inputfilename: str = args[1]
    with open(inputfilename) as inputfile:
        for line in inputfile:
            splittedline: List[str] = line.strip().split(", ")

            item_id = int(splittedline[0])  # Convert to int for SQL query
            quantity_item = int(splittedline[1])
            employee_id = int(splittedline[2])
            date = splittedline[3]

            conn = sqlite3.connect("bgumart.db")
            cursor = conn.cursor()
            try:
                # Fetch current quantity of the product
                cursor.execute('''
                    SELECT quantity
                    FROM products
                    WHERE id = ?
                ''', (item_id,))
                result = cursor.fetchone()

                if result is None:
                    print(f"Error: Product with ID {item_id} does not exist.")
                    continue

                current_quantity = result[0]

                # Check if the operation is valid
                if current_quantity + quantity_item >= 0:
                    # Update product quantity
                    cursor.execute('''
                        UPDATE products
                        SET quantity = quantity + ?
                        WHERE id = ?
                    ''', (quantity_item, item_id))

                    # Insert into activities table
                    cursor.execute('''
                        INSERT INTO activities (product_id, quantity, activator_id, date)
                        VALUES (?, ?, ?, ?)
                    ''', (item_id, quantity_item, employee_id, date))

                    # Commit the changes
                    conn.commit()
                else:
                    print(f"Error: Insufficient stock for product ID {item_id}.")

            except sqlite3.IntegrityError as e:
                print(f"Error: Could not process activity. {e}")
            finally:
                # Ensure the connection is closed
                conn.close()
                
                
if __name__ == '__main__':
    main(sys.argv)