import inspect


def orm(cursor, dto_type):
    # Using inspect.signature() instead of inspect.getargspec()
    signature = inspect.signature(dto_type.__init__)  # Get the signature of the constructor
    args = [param.name for param in signature.parameters.values()]
    
    # The first argument of the constructor will be 'self', so we skip it
    args = args[1:]

    # Gets the names of the columns returned in the cursor
    col_names = [column[0] for column in cursor.description]

    # Map them into the position of the corresponding constructor argument
    col_mapping = [col_names.index(arg) for arg in args]
    
    return [row_map(row, col_mapping, dto_type) for row in cursor.fetchall()]


def row_map(row, col_mapping, dto_type):
    ctor_args = [row[idx] for idx in col_mapping]
    return dto_type(*ctor_args)


class Dao(object):
    def __init__(self, dto_type, conn):
        self._conn = conn
        self._dto_type = dto_type

        # dto_type is a class, its __name__ field contains a string representing the name of the class.
        self._table_name = dto_type.__name__.lower() + 's'

    def insert(self, dto_instance):
        ins_dict = vars(dto_instance)

        column_names = ','.join(ins_dict.keys())
        params = list(ins_dict.values())
        qmarks = ','.join(['?'] * len(ins_dict))

        stmt = 'INSERT INTO {} ({}) VALUES ({})' \
            .format(self._table_name, column_names, qmarks)

        self._conn.execute(stmt, params)

    def find_all(self):
        c = self._conn.cursor()
        c.execute('SELECT * FROM {}'.format(self._table_name))
        return orm(c, self._dto_type)
    
    def find(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
 
        stmt = 'SELECT * FROM {} WHERE {}' \
               .format(self._table_name, ' AND '.join([col + '=?' for col in column_names]))
 
        c = self._conn.cursor()
        c.execute(stmt, params)
        return orm(c, self._dto_type)

    def delete(self, **keyvals):
        column_names = keyvals.keys()
        params = list(keyvals.values())
 
        stmt = 'DELETE FROM {} WHERE {}' \
               .format(self._table_name,' AND '.join([col + '=?' for col in column_names]))
 
        self._conn.cursor().execute(stmt, params)


    def update(self, **updates):
        # Ensure 'id' is not part of the updates to be set
        id=updates.pop('id', None)  # Remove 'id' if it's in the updates

        # Unpack the updates
        set_clause = ', '.join([f"{key} = ?" for key in updates.keys()])
        params = list(updates.values())  # Only the fields to be updated (without 'id')

        # Create the SQL statement to update the record
        stmt = f"UPDATE {self._table_name} SET {set_clause} WHERE id = ?"
    
        # We need to pass the id as the last parameter for the WHERE clause
        params.append(id)  # Assuming 'id' is still passed for the WHERE condition
    
        # Execute the query
        self._conn.execute(stmt, params)
        


