import sqlite3
import os

col_dict = {"jobs": {"id": 0, "partid": 1, "capacity": 2, "completed": 3, "scrap": 4},
            "workcenters": {"id": 0, "workid": 1, "jobid": 2, "feed_wheel_diameter": 3, "output_toggle": 4,
                            "threshold": 5, "state": 6, "rate": 7, "input_length": 8, "output_detected": 9,
                            "finished_length_raw": 10, "time_started": 11, "time_ended": 12},
            "parts": {"id": 0, "part_length": 1, "part_num": 2, "part_type": 3, "part_bool": 4}}
tables = {0: "jobs", 1: "workcenters", 2: "parts"}
bool_vals = {"parts": 4, "workcenters": 4}


class DataBase:

    def __init__(self, file_path='C:\\Users\\tlham\\Documents\\spring.db'):
        if os.path.splitext(file_path)[1] != ".db":
            raise RuntimeError("Invalid file")
        self.__file_path = file_path
        if os.path.exists(self.__file_path):
            self.__initialized = True
        else:
            self.__initialized = False

    # create tables and insert some sample rows
    def initialize_db(self):
        if self.__initialized:
            return RuntimeError('Db already initialized')
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        try:
            c.execute('''CREATE TABLE parts (id varchar(30) PRIMARY KEY, part_length decimal(5, 2) DEFAULT 0.0, 
            part_num varchar(6), part_type varchar(50), part_bool boolean DEFAULT 0 CHECK (part_bool IN (0, 1)))''')
            c.execute('''INSERT INTO parts (id, part_length, part_num, part_type, part_bool) VALUES ('1', 12.32, 
            'aa00aa', 'extender', 1)''')
            c.execute('''INSERT INTO parts (id, part_num, part_type) VALUES ('2', 'aa00aa', 'pin')''')
            c.execute('''INSERT INTO parts (id, part_length, part_num, part_type, part_bool) VALUES ('3', 7.77, 
            'ac01aa', 'something', 1)''')
            c.execute('''INSERT INTO parts (id, part_num, part_type) VALUES ('4', 'ba00ab', 'other')''')

            c.execute('''CREATE TABLE jobs (id varchar(30) PRIMARY KEY, partid varchar(30), capacity int, completed 
            int DEFAULT 0, scrap int DEFAULT 0, FOREIGN KEY (partid) REFERENCES parts (id))''')
            c.execute('''INSERT INTO jobs (id, partid, capacity) VALUES ('1', '1', 50)''')
            c.execute('''INSERT INTO jobs (id, partid, capacity, scrap) VALUES ('2', '2', 100, 45)''')
            c.execute('''INSERT INTO jobs (id, partid, capacity) VALUES ('3', '1', 120)''')
            c.execute('''INSERT INTO jobs (id, partid, capacity, completed) VALUES ('4', '3', 25, 20)''')

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
            conn.close()
            os.remove(self.__file_path)
            return err
        conn.close()
        self.__initialized = True
        return None

    # returns True if the database has been initialized
    def is_initialized(self):
        return self.__initialized

    # return a row with the matching id from the specified table or None
    # also returns an error if one occurred
    def get(self, table, rid):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        if table not in tables.values():
            return None, RuntimeError("Invalid table")
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM {} WHERE id = ?".format(table), (rid,))
        except sqlite3.Error as err:
            conn.close()
            return None, err
        row = c.fetchone()
        if row is not None:
            row = list(row)
            if table in bool_vals:
                row[bool_vals[table]] = bool(row[bool_vals[table]])
            row = tuple(row)
        conn.close()
        return row, None

    # insert a job into the table and return an error if one occurred
    def insert(self, table, rid, **columns):
        if not self.__initialized:
            return RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        if table not in tables.values():
            return None, RuntimeError("Invalid table")
        insert_cols = "id"
        insert_values = "?"
        for k in columns.keys():
            if k not in col_dict[table]:
                return None, RuntimeError("Invalid column name")
            insert_cols += ", " + k
            insert_values += ", ?"
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO {} ({}) VALUES ({})'''.format(table, insert_cols, insert_values),
                      (rid,) + tuple(columns.values()))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return err
        conn.close()
        return None

    # update a job with the matching id and return the old row or None
    # returns an error if one occurred
    def update(self, table, rid, **columns):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        if table not in tables.values():
            return None, RuntimeError("Invalid table")
        col_list = []
        for k in columns.keys():
            if k not in col_dict[table]:
                return None, RuntimeError("Invalid column name")
            col_list.append(k + " = ?")
        update_str = ", ".join(col_list)
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM {} WHERE id = ?".format(table), (rid,))
            row = c.fetchone()
            if row is not None:
                row = list(row)
                if table in bool_vals:
                    row[bool_vals[table]] = bool(row[bool_vals[table]])
                row = tuple(row)
            c.execute("UPDATE {} SET {} WHERE id = ?".format(table, update_str), tuple(columns.values()) + (rid,))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row, None

    # delete a job from the table and return the row that was deleted or None
    # also returns an error if one occurred
    def delete(self, table, rid):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        if table not in tables.values():
            return None, RuntimeError("Invalid table")
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM {} WHERE id = ?".format(table), (rid,))
            row = c.fetchone()
            if row is not None:
                row = list(row)
                if table in bool_vals:
                    row[bool_vals[table]] = bool(row[bool_vals[table]])
                row = tuple(row)
            c.execute("DELETE FROM {} WHERE id = ?".format(table), (rid,))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row, None

    def clear_table(self, table):
        if not self.__initialized:
            return RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        if table not in tables.values():
            return None, RuntimeError("Invalid table")
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        try:
            c.execute("DELETE FROM {}".format(table))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return err
        conn.close()
        return None

    def exists(self, table, rid):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        if table not in tables.values():
            return None, RuntimeError("Invalid table")
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        try:
            c.execute("SELECT COUNT(*) FROM {} WHERE id = ?".format(table), (rid,))
            count = c.fetchone()[0]
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return count != 0, None

    def workcenter_addr_to_id(self, addr):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
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

    def workcenter_id_to_addr(self, workid):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        try:
            conn = sqlite3.connect(self.__file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
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
