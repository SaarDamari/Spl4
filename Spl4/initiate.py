from persistence import *
import sys
import os
import sqlite3
from typing import List


def add_branche(splittedline: List[str], repo: Repository):
    branch_id = int(splittedline[1])
    location = splittedline[2]
    num_employees = int(splittedline[3])
    repo.branches.insert(Branche(branch_id, location, num_employees))


def add_supplier(splittedline: List[str], repo: Repository):
    supplier_id = int(splittedline[1])
    name = splittedline[2]
    phone = splittedline[3]
    repo.suppliers.insert(Supplier(supplier_id, name, phone))

def add_product(splittedline: List[str], repo: Repository):
    product_id = int(splittedline[1])
    description = splittedline[2]
    price = float(splittedline[3])
    quantity = int(splittedline[4])
    repo.products.insert(Product(product_id, description, price, quantity))


def add_employee(splittedline: List[str], repo: Repository):
    employee_id = int(splittedline[1])
    name = splittedline[2]
    salary = float(splittedline[3])
    branch_id = int(splittedline[4])
    repo.employees.insert(Employee(employee_id, name, salary, branch_id))


# Mapping for adder functions
adders = {
    "B": add_branche,
    "S": add_supplier,
    "P": add_product,
    "E": add_employee
}


def main(args: List[str]):
    if len(args) < 2:
       print("Usage: python script.py <input_file>")
       sys.exit(1)

    inputfilename = args[1]

    # Reinitialize the repository
    #if os.path.isfile("bgumart.db"):
    #    os.remove("bgumart.db")
    
    with open("bgumart.db", "w"):
        pass 
    repo.create_tables()
    try:
        with open(inputfilename) as inputfile:
            for line in inputfile:
                splittedline: List[str] = line.strip().split(",")
                adder_function = adders.get(splittedline[0])
                if adder_function:
                    adder_function(splittedline, repo)

    except FileNotFoundError:
        print(f"Error: File '{inputfilename}' not found.")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # Closing the repository connection
    #repo._close()


if __name__ == '__main__':
    main(sys.argv)
