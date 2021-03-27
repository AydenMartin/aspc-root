import sqlite3
import os.path as path

job_cols = {"id": 0, "prog": 1, "scrap": 2, "rate": 3}
ws_cols = {"id": 0, "jobid": 1, "partnum": 2, "capacity": 3, "conversion": 4, "threshold": 5, "status": 6}
tables = {0: "jobs", 1: "workcenters"}


class DataBase:

    def __init__(self, file_path='C:\\Users\\tlham\\Documents\\spring.db'):
        if path.splitext(file_path)[1] != ".db":
            raise RuntimeError("Invalid file")
        self.file_path = file_path
        if path.exists(self.file_path):
            self.__initialized = True
        else:
            self.__initialized = False

    # create tables and insert some sample rows
    def initialize_db(self):
        if self.__initialized:
            return RuntimeError('Db already initialized')
        try:
            conn = sqlite3.connect(self.file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        c.execute('''CREATE TABLE jobs (id varchar(30) PRIMARY KEY, prog decimal(5, 2),
         scrap int, rate decimal(5, 2))''')
        c.execute('''INSERT INTO jobs (id, prog, scrap, rate) VALUES ('1', 6.00, 50, 3.14)''')
        c.execute('''INSERT INTO jobs (id, prog, scrap, rate) VALUES ('2', 7.45, 50, 0)''')
        c.execute('''INSERT INTO jobs (id, prog, scrap, rate) VALUES ('3', 3.60, 50, 4.56)''')
        c.execute('''INSERT INTO jobs (id, prog, scrap, rate) VALUES ('4', 12.50, 50, 5.54)''')

        c.execute('''CREATE TABLE workcenters (id varchar(30) PRIMARY KEY, jobid varchar(30), partnum varchar(6), 
        capacity int, conversion decimal(5, 2), threshold int, status varchar(50), FOREIGN KEY (jobid) REFERENCES 
        jobs (id))''')
        c.execute('''INSERT INTO workcenters (id, capacity, conversion,threshold, status) 
        VALUES ('1', 250, 12.3, 50, 'IDLE')''')
        c.execute('''INSERT INTO workcenters (id, capacity, conversion, threshold, status) 
        VALUES ('2', 124, 6.67, 50, 'IDLE')''')
        c.execute('''INSERT INTO workcenters (id, capacity, conversion, threshold, status) 
        VALUES ('3', 225, 9.00, 50, 'IDLE')''')
        c.execute('''INSERT INTO workcenters (id, capacity, conversion, threshold, status) 
        VALUES ('4', 100, 5.55, 50, 'IDLE')''')
        conn.commit()
        conn.close()
        self.__initialized = True
        return None

    # returns True if the database has been initialized
    def is_initialized(self):
        return self.__initialized

    # return a row with the matching id from the specified table or None
    # also returns an error if one occurred
    def get(self, table, id):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        try:
            conn = sqlite3.connect(self.file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        if type(table) == int and table < len(tables):
            table = tables[table]
        try:
            c.execute("SELECT * FROM {} WHERE id = '{}'".format(table, id))
        except sqlite3.Error as err:
            conn.close()
            return None, err
        row = c.fetchone()
        conn.close()
        return row, None

    # insert a job into the table and return an error if one occurred
    def insert(self, table, id, **columns):
        if not self.__initialized:
            return RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        insert_cols = "id"
        insert_values = "'" + str(id) + "'"
        for k in columns.keys():
            if columns[k] is None:
                columns[k] = "NULL"
            elif type(columns[k]) == str:
                columns[k] = "'" + columns[k] + "'"
            else:
                columns[k] = str(columns[k])
        if len(columns) > 0:
            insert_cols += ", " + ", ".join(columns.keys())
            insert_values += ", " + ", ".join(columns.values())
        try:
            conn = sqlite3.connect(self.file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        try:
            c.execute('''INSERT INTO {} ({}) VALUES ({})'''.format(table, insert_cols, insert_values))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return err
        conn.close()
        return None

    # update a job with the matching id and return the old row or None
    # returns an error if one occurred
    def update(self, table, id, **columns):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        if type(table) == int and table < len(tables):
            table = tables[table]
        col_list = []
        for k in columns.keys():
            if columns[k] is None:
                col_list.append(k + " = NULL")
            elif type(columns[k]) == str:
                col_list.append(k + " = '" + columns[k] + "'")
            else:
                col_list.append(k + " = " + str(columns[k]))
        update_str = ", ".join(col_list)
        try:
            conn = sqlite3.connect(self.file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM {} WHERE id = '{}'".format(table, id))
            row = c.fetchone()
            c.execute("UPDATE {} SET {} WHERE id = '{}'".format(table, update_str, id))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row, None

    # delete a job from the table and return the row that was deleted or None
    # also returns an error if one occurred
    def delete(self, table, id):
        if not self.__initialized:
            return None, RuntimeError("DB not initialized")
        try:
            conn = sqlite3.connect(self.file_path)
        except sqlite3.Error as err:
            return None, err
        c = conn.cursor()
        if type(table) == int and table < len(tables):
            table = tables[table]
        try:
            c.execute("SELECT * FROM {} WHERE id = '{}'".format(table, id))
            row = c.fetchone()
            c.execute("DELETE FROM {} WHERE id = '{}'".format(table, id))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return None, err
        conn.close()
        return row, None

    def clear_tables(self):
        if not self.__initialized:
            return RuntimeError("DB not initialized")
        try:
            conn = sqlite3.connect(self.file_path)
        except sqlite3.Error as err:
            return err
        c = conn.cursor()
        try:
            for t in tables:
                c.execute("DELETE FROM {}".format(tables[t]))
            conn.commit()
        except sqlite3.Error as err:
            conn.close()
            return err
        conn.close()
        return None
