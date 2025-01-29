from persistence import *
import sqlite3
import inspect
def main():
    conn = sqlite3.connect("bgumart.db")
    cursor=conn.cursor()
    employees = Dao(Employee, conn)
    suppliers = Dao(Supplier, conn)
    products = Dao(Product, conn)
    branches = Dao(Branche, conn)
    cursor = conn.cursor()

    # Print Activities table
    print("Activities")
    cursor.execute('''
        SELECT *
        FROM activities
        ORDER BY date
    ''')
    for row in cursor.fetchall():
        print(row)
    print()
    # Print other tables: branches, employees, products, suppliers
    for table in [branches,employees,products,suppliers,products]:
        print((table._table_name).capitalize())
        result=table.find_all()
        
        for row in result:
            print(row)
        print()

    # Print Employees report
    print("Employees Report")
    cursor.execute('''
        SELECT E.name, E.salary, B.location, COALESCE(SUM(ABS(A.quantity * P.price)), 0) AS total_sales_income
        FROM employees AS E
        LEFT JOIN branches AS B ON E.branche = B.id
        LEFT JOIN activities AS A ON A.activator_id = E.id AND A.quantity < 0
        LEFT JOIN products AS P ON P.id = A.product_id
        GROUP BY E.name, E.salary, B.location
        ORDER BY E.name;
    ''')
    for row in cursor.fetchall():
        print(row)
    print()

    # Print Activities report
    print("Activities Report")
    cursor.execute('''
        SELECT activities.date, products.description, activities.quantity,
               CASE WHEN activities.quantity < 0 THEN employees.name ELSE 'None' END AS seller_name,
               CASE WHEN activities.quantity > 0 THEN suppliers.name ELSE 'None' END AS supplier_name
        FROM activities
        LEFT JOIN products ON activities.product_id = products.id
        LEFT JOIN employees ON activities.activator_id = employees.id
        LEFT JOIN suppliers ON activities.activator_id = suppliers.id
        ORDER BY activities.date;
    ''')
    for row in cursor.fetchall():
        print(row)

    # Close the connection
    conn.close()

if __name__ == '__main__':
    main()
