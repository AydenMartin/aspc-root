import sqlite3
import os
from typing import Union, Optional, Tuple, Any, List, Dict


class DataBase:
    """
    This class is used to represent a SQLite database with tables for jobs, parts, and workcenters

    Attributes:
        file_path (str): The file path that the database is stored at
        initialized (bool): Indicates if the database's tables have been created
        col_dict (dict): Stores the columns of each table and their associated index number
        tables (dict): Stores the index number that each table is associated with
        bool_vals (dict): Indicates which columns need to converted to booleans
    """

    __col_dict = {"jobs": {"id": 0, "partid": 1, "capacity": 2, "completed": 3, "scrap": 4},
                  "workcenters": {"id": 0, "workid": 1, "jobid": 2, "feed_wheel_diameter": 3, "output_toggle": 4,
                                  "threshold": 5, "state": 6, "rate": 7, "input_length": 8, "output_detected": 9,
                                  "finished_length_raw": 10, "time_started": 11, "time_ended": 12},
                  "parts": {"id": 0, "part_length": 1, "part_num": 2, "part_type": 3, "part_bool": 4}}
    __tables = {0: "jobs", 1: "workcenters", 2: "parts"}
    __bool_vals = {"parts": 4, "workcenters": 4}

    def cols(self) -> Dict[str, Dict[str, int]]:
        """
        Accesses the columns used by all spring databases, which are protected from modification

        :return: A copy of the column dictionary
        """
        return self.__col_dict.copy()

    def __init__(self, file_path: str = 'C:\\Users\\tlham\\Documents\\spring.db'):
        """
        Constructor for the DataBase class.  When the object is created, the database will be considered initialized
        if the given file path already exists.

        :param file_path: the file path that the database will be stored at
        :raises RuntimeError: if the file is not a db file
        """
        if os.path.splitext(file_path)[1] != ".db":
            raise RuntimeError("Invalid file")
        self.__file_path = file_path
        if os.path.exists(self.__file_path):
            self.__initialized = True
        else:
            self.__initialized = False

    def initialize_db(self) -> Optional[Exception]:
        """
        Creates the database file, creates all tables, and adds sample values.  This method should be called before any
        other database methods are used, and should not be called on an already initialized database

        :return: None if initialization was successful, or the error that occurred
        """
        # Return error if the database has already been initialized
        if self.__initialized:
            return RuntimeError('Db already initialized')
        # Return error if the file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        try:
            # Create the parts table and add sample values
            c.execute('''CREATE TABLE parts (id varchar(30) PRIMARY KEY, part_length decimal(5, 2) DEFAULT 0.0, 
            part_num varchar(6), part_type varchar(50), part_bool boolean DEFAULT 0 CHECK (part_bool IN (0, 1)))''')
            c.execute('''INSERT INTO parts (id, part_length, part_num, part_type, part_bool) VALUES ('1', 12.32, 
            'aa00aa', 'extender', 1)''')
            c.execute('''INSERT INTO parts (id, part_num, part_type) VALUES ('2', 'aa00aa', 'pin')''')
            c.execute('''INSERT INTO parts (id, part_length, part_num, part_type, part_bool) VALUES ('3', 7.77, 
            'ac01aa', 'something', 1)''')
            c.execute('''INSERT INTO parts (id, part_num, part_type) VALUES ('4', 'ba00ab', 'other')''')

            # Create the jobs table and add sample values
            c.execute('''CREATE TABLE jobs (id varchar(30) PRIMARY KEY, partid varchar(30), capacity int, completed 
            int DEFAULT 0, scrap int DEFAULT 0, FOREIGN KEY (partid) REFERENCES parts (id))''')
            c.execute('''INSERT INTO jobs (id, partid, capacity) VALUES ('1', '1', 50)''')
            c.execute('''INSERT INTO jobs (id, partid, capacity, scrap) VALUES ('2', '2', 100, 45)''')
            c.execute('''INSERT INTO jobs (id, partid, capacity) VALUES ('3', '1', 120)''')
            c.execute('''INSERT INTO jobs (id, partid, capacity, completed) VALUES ('4', '3', 25, 20)''')

            # Create the workcenter table and add sample values
            c.execute('''CREATE TABLE workcenters (id varchar(15) PRIMARY KEY, workid varchar(30) UNIQUE, 
            jobid varchar(30), feed_wheel_diameter decimal(5, 2), output_toggle boolean DEFAULT 0 CHECK (
            output_toggle IN (0, 1)), threshold int DEFAULT 50, state int DEFAULT 0, rate decimal(5, 2) DEFAULT 0.0, 
            input_length int, output_detected int, finished_length_raw int, time_started int, time_ended int, 
            FOREIGN KEY (jobid) REFERENCES jobs (id))''')
            c.execute('''INSERT INTO workcenters (id, state, feed_wheel_diameter, output_toggle) VALUES ('2.2.2.2', 0, 
            2.34, 1)''')
            c.execute('''INSERT INTO workcenters (id, jobid, state, threshold) VALUES ('0.0.0.0', '1', 1, 45)''')
            c.execute('''INSERT INTO workcenters (id, jobid, state) VALUES ('1.2.3.4', '2', 0)''')
            c.execute('''INSERT INTO workcenters (id, workid, state, output_toggle) VALUES ('127.0.0.1', '4', 1, 1)''')
            conn.commit()
        except sqlite3.Error as err:
            # Remove created file if there was an error during initialization
            conn.close()
            os.remove(self.__file_path)
            return err
        conn.close()
        self.__initialized = True
        return None

    def is_initialized(self) -> bool:
        """
        Used to indicate if the database has been initialized and other database methods can be used

        :return: a boolean value
        """
        return self.__initialized

    def get(self, table: Union[str, int], rid: str) -> Tuple[Optional[Tuple[Any, ...]], Optional[Exception]]:
        """
        Connects to the database and retrieves one row from a specified table

        :param table: The table that will be operated on
        :param rid: The primary key value used to find a row
        :return: The first value is a row tuple or None if no row was found or there was an error. The second value is the error that occurred or None if the get was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        # Convert index number to table name if needed
        if type(table) == int and table < len(self.__tables):
            table = self.__tables[table]
        # Return error if the table name is invalid
        if table not in self.__tables.values():
            return None, RuntimeError("Invalid table")
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        # Execute SQL statement
        try:
            c.execute("SELECT * FROM {} WHERE id = ?".format(table), (rid,))
        except sqlite3.Error as err:
            conn.close()
            return None, err
        row = c.fetchone()
        # Convert boolean values if needed
        if row is not None:
            row = list(row)
            if table in self.__bool_vals:
                row[self.__bool_vals[table]] = bool(row[self.__bool_vals[table]])
            row = tuple(row)
        conn.close()
        return row, None

    def get_all(self, table: Union[str, int]) -> Tuple[Optional[List[Tuple[Any, ...]]], Optional[Exception]]:
        """
        Connects to the database and retrieves all rows in a specified table

        :param table: The table to be operated on
        :return: The first value is a list containing all row tuples or None if there was an error. The second value is the error that occurred or None if the get was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        # Convert index number to table name if needed
        if type(table) == int and table < len(self.__tables):
            table = self.__tables[table]
        # Return error if the table name is invalid
        if table not in self.__tables.values():
            return None, RuntimeError("Invalid table")
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        # Execute SQL statement
        try:
            c.execute("SELECT * FROM {}".format(table))
        except sqlite3.Error as err:
            conn.close()
            return None, err
        rows = c.fetchall()
        # Convert boolean values if needed
        if table in self.__bool_vals:
            for index, row in enumerate(rows):
                row = list(row)
                row[self.__bool_vals[table]] = bool(row[self.__bool_vals[table]])
                rows[index] = tuple(row)
        conn.close()
        return rows, None

    def insert(self, table: Union[str, int], rid: str, **columns: Any) -> Optional[Exception]:
        """
        Inserts a new row into a table

        :param table: The table to be operated on
        :param rid: The primary key value of the new row
        :param columns: All non-PK values to be inserted
        :return: An error that occurred or none if the insert was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return RuntimeError("DB not initialized")
        # Convert index number to table name if needed
        if type(table) == int and table < len(self.__tables):
            table = self.__tables[table]
        # Return error if the table name is invalid
        if table not in self.__tables.values():
            return RuntimeError("Invalid table")
        # Construct lists of columns and values
        insert_cols = "id"
        insert_values = "?"
        for k in columns.keys():
            # Return error if column name is invalid
            if k not in self.__col_dict[table]:
                return RuntimeError("Invalid column name")
            insert_cols += ", " + k
            insert_values += ", ?"
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        # Execute SQL statement
        try:
            c.execute('''INSERT INTO {} ({}) VALUES ({})'''.format(table, insert_cols, insert_values),
                      (rid,) + tuple(columns.values()))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return err
        conn.close()
        return None

    def update(self, table: Union[str, int], rid: str, **columns: Any) -> Tuple[Optional[Tuple[Any, ...]],
                                                                                Optional[Exception]]:
        """
        Connects to the database and updates a single row in a specified table

        :param table: The table to be operated on
        :param rid: The primary key value used to find the row to update
        :param columns: All columns that will be updated
        :return: The first value is row's previous state before being updated or None if no row was updated or there was an error.  The second value is the error that occurred or None if the update was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        # Convert index number to table name if needed
        if type(table) == int and table < len(self.__tables):
            table = self.__tables[table]
        # Return error if the table name is invalid
        if table not in self.__tables.values():
            return None, RuntimeError("Invalid table")
        # Construct list of columns
        col_list = []
        for k in columns.keys():
            if k not in self.__col_dict[table]:
                # Return error if column name is invalid
                return None, RuntimeError("Invalid column name")
            col_list.append(k + " = ?")
        update_str = ", ".join(col_list)
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        # Execute SQL statements
        try:
            # Get old row data
            c.execute("SELECT * FROM {} WHERE id = ?".format(table), (rid,))
            row = c.fetchone()
            # Convert boolean values if needed
            if row is not None:
                row = list(row)
                if table in self.__bool_vals:
                    row[self.__bool_vals[table]] = bool(row[self.__bool_vals[table]])
                row = tuple(row)
            # Update row with new data
            c.execute("UPDATE {} SET {} WHERE id = ?".format(table, update_str), tuple(columns.values()) + (rid,))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row, None

    def delete(self, table: Union[str, int], rid: str) -> Tuple[Optional[Tuple[Any, ...]], Optional[Exception]]:
        """
        Connects to the database and deletes a single row from a specified table

        :param table: The table to be operated on
        :param rid: The primary key value used to find the row to delete
        :return: The first value is the row that was deleted or None if no row was found or there was an error. The second value is the error that occurred or None if the delete was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        # Convert index number to table name if needed
        if type(table) == int and table < len(self.__tables):
            table = self.__tables[table]
        # Return error if the table name is invalid
        if table not in self.__tables.values():
            return None, RuntimeError("Invalid table")
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        # Execute SQL statements
        try:
            # Get row data
            c.execute("SELECT * FROM {} WHERE id = ?".format(table), (rid,))
            row = c.fetchone()
            # Convert boolean values if needed
            if row is not None:
                row = list(row)
                if table in self.__bool_vals:
                    row[self.__bool_vals[table]] = bool(row[self.__bool_vals[table]])
                row = tuple(row)
            # Delete the row
            c.execute("DELETE FROM {} WHERE id = ?".format(table), (rid,))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row, None

    def clear_table(self, table: Union[str, int]) -> Optional[Exception]:
        """
        Connects to the databases and clears all rows from a specified table

        :param table: The table to be cleared
        :return: An error that occurred or None if the delete was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return RuntimeError("DB not initialized")
        # Convert index number to table name if needed
        if type(table) == int and table < len(self.__tables):
            table = self.__tables[table]
        # Return error if the table name is invalid
        if table not in self.__tables.values():
            return RuntimeError("Invalid table")
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        # Execute SQL statement
        try:
            c.execute("DELETE FROM {}".format(table))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return err
        conn.close()
        return None

    def exists(self, table: Union[str, int], rid: str) -> Tuple[Optional[bool], Optional[Exception]]:
        """
        Connects to the database and determines if the given primary key already exists in the specified table

        :param table: The table to look in
        :param rid: The primary key value to look for
        :return: The first value is True if the primary key was found, False if it was not, or None if an error occurred. The second value is the error that occurred or None if the get was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        # Convert index number to table name if needed
        if type(table) == int and table < len(self.__tables):
            table = self.__tables[table]
        # Return error if the table name is invalid
        if table not in self.__tables.values():
            return None, RuntimeError("Invalid table")
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        # Execute SQL statement
        try:
            c.execute("SELECT COUNT(*) FROM {} WHERE id = ?".format(table), (rid,))
            count = c.fetchone()[0]
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return count != 0, None

    def workcenter_addr_to_id(self, addr: str) -> Tuple[Optional[str], Optional[Exception]]:
        """
        Takes a workcenter ip address and finds the associated id

        :param addr: The ip address to look for
        :return: The first value is the id that was found or None if the ip address is not in the table or there was an error. The second value is the error that occurred or None if the get was successful.
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        # Execute SQL statement
        try:
            c.execute("SELECT workid FROM workcenters WHERE id = ?", (addr,))
            row = c.fetchone()
            if row is None:
                return None, None
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row[0], None

    def workcenter_id_to_addr(self, workid: str) -> Tuple[Optional[str], Optional[Exception]]:
        """
        Takes a workcenter id and finds the associated ip address

        :param workid: The id to look for
        :return: The first value is the ip address that was found or None if the id is not in the table or there was an error.  The second value is the error that occurred or None if the get was successful
        """
        # Return error if the database hasn't been initialized
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        # Return error if file path could not be reached
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        # Execute SQL statement
        try:
            c.execute("SELECT id FROM workcenters WHERE workid = ?", (workid,))
            row = c.fetchone()
            if row is None:
                return None, None
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row[0], None
